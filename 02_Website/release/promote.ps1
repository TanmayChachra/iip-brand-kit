# Promote staging to PRODUCTION (Pages project iip-site, branch main). The only script allowed to deploy to production,
# and only after the owner types GO LIVE. -DryRun does everything except merge, tag and deploy (and skips the prompt).
param([switch]$DryRun)
. "$PSScriptRoot\lib.ps1"
function Refuse([string]$why) { Write-Host "REFUSED: $why" -ForegroundColor Red; exit 1 }

# 1. Gates
$branch = (git -C $Repo rev-parse --abbrev-ref HEAD).Trim()
if ($branch -ne 'staging') { Refuse "current branch is '$branch', must be staging" }
# Only the website source decides cleanliness: brand kit, notes and test output may change freely.
$SitePaths = @('02_Website/site-v2/src','02_Website/site-v2/public','02_Website/site-v2/scripts','02_Website/site-v2/astro.config.mjs','02_Website/site-v2/package.json','02_Website/site-v2/package-lock.json','02_Website/site-v2/.env.staging','02_Website/site-v2/.env.production','02_Website/release')
if (((git -C $Repo status --porcelain -- $SitePaths) | Out-String).Trim()) { Refuse 'website source is not committed (commit the site changes on the staging branch first)' }
$head = (git -C $Repo rev-parse HEAD).Trim()
if (-not (Test-Path "$Release\last-checks.json")) { Refuse 'no last-checks.json, run deploy-staging.ps1 first' }
$c = Get-ChecksJson
if ($c.status -ne 'PASS') { Refuse "last checks are $($c.status)" }
if ($c.commit -ne $head) { Refuse "last checks were for commit $($c.commit.Substring(0,8)), HEAD is $($head.Substring(0,8)). Run deploy-staging.ps1 again" }
if (((Get-Date).ToUniversalTime() - ([datetime]$c.time).ToUniversalTime()).TotalHours -gt 24) { Refuse 'last checks are older than 24 hours' }
if (-not (Test-Path "$Release\last-staging.json")) { Refuse 'staging was never deployed from this machine, run deploy-staging.ps1' }
$s = Get-Content "$Release\last-staging.json" -Raw | ConvertFrom-Json
if ($s.commit -ne $head) { Refuse 'staging was deployed from a different commit, run deploy-staging.ps1' }
Write-Host '== staging smoke'
try { Invoke-Native node @('release/smoke.mjs', $StagingUrl, 'staging') "$Repo\02_Website" | Out-Null } catch { Refuse 'staging smoke failed' }
& git -C $Repo merge-base --is-ancestor main staging
if ($LASTEXITCODE -ne 0) { Refuse 'main is not an ancestor of staging (fast-forward impossible). Merge main into staging first' }

# 2. Human gate
if ($DryRun) { Write-Host 'DRY RUN: skipping the GO LIVE prompt' } else {
  Write-Host "About to publish commit $($head.Substring(0,8)) to $ProdUrl."
  if ((Read-Host 'Type GO LIVE to continue') -ne 'GO LIVE') { Refuse 'GO LIVE not typed' }
}

# 3. Merge (ff only), build, check
$tag = 'prod-' + (Get-Date -Format 'yyyyMMdd-HHmm')
if ($DryRun) { Write-Host "DRY RUN: would merge staging into main (ff-only) and tag $tag" } else {
  Invoke-Native git @('checkout', 'main') | Out-Null
  Invoke-Native git @('merge', '--ff-only', 'staging') | Out-Null
}
Write-Host '== build production'
Invoke-Native npm @('run', 'build:production') $Site | Out-Null
$idx = Get-Content "$Site\dist-production\index.html" -Raw
if ($idx -notmatch 'rel="canonical" href="https://isapurindustrialpark\.com/"' -or $idx -notmatch 'GTM-KMBRGVSD' -or $idx -match 'data-staging-ribbon') { if (-not $DryRun) { Invoke-Native git @('checkout', 'staging') | Out-Null }; Refuse 'production build failed sanity (canonical, GTM or ribbon)' }
Write-Host '== checks on dist-production'
try { Invoke-Native node @('release/checks.mjs', 'site-v2/dist-production', 'production') "$Repo\02_Website" | Out-Null } catch { if (-not $DryRun) { Invoke-Native git @('checkout', 'staging') | Out-Null }; Refuse 'production checks failed (main was fast-forwarded locally only, nothing deployed)' }
if ($DryRun) { Write-Host "DRY RUN PASS: would tag $tag, deploy site-v2/dist-production to iip-site --branch main, smoke $ProdUrl, log RELEASES.md. Nothing merged, tagged or deployed."; exit 0 }

# 4. Tag, deploy, smoke, log
Invoke-Native git @('tag', $tag) | Out-Null
$out = Invoke-Native npx @('wrangler', 'pages', 'deploy', 'site-v2/dist-production', '--project-name', 'iip-site', '--branch', 'main', '--commit-hash', $head, '--commit-message', $tag) "$Repo\02_Website"
$m = [regex]::Match($out, 'https://([a-z0-9]+)\.iip-site\.pages\.dev')
Start-Sleep -Seconds 5
$smoke = 'PASS'
try { Invoke-Native node @('release/smoke.mjs', $ProdUrl, 'production') "$Repo\02_Website" | Out-Null } catch { $smoke = 'FAIL' ; Write-Host 'PRODUCTION SMOKE FAILED. Run rollback.ps1 now.' -ForegroundColor Red }
"| $(Get-Date -Format 'yyyy-MM-dd HH:mm') | $($head.Substring(0,8)) | $tag | $($m.Groups[1].Value) | $($m.Value) | smoke $smoke |" | Add-Content -Encoding utf8 "$Release\RELEASES.md"
# Keep main == production and staging a fast-forward of main: commit the log line on main, then move staging up to it.
Invoke-Native git @('add', '02_Website/release/RELEASES.md') | Out-Null
Invoke-Native git @('commit', '-m', "Release $tag") | Out-Null
Invoke-Native git @('checkout', 'staging') | Out-Null
Invoke-Native git @('merge', '--ff-only', 'main') | Out-Null
Write-Host "LIVE: $ProdUrl  tag $tag  deployment $($m.Value)  smoke $smoke. Push main, staging and tags to GitHub: git push origin main staging --tags"
if ($smoke -ne 'PASS') { exit 1 }
