# Deploy the current working tree to STAGING only (Pages project iip-staging). The only deploy command helpers may run.
# Usage: powershell -File 02_Website/release/deploy-staging.ps1
. "$PSScriptRoot\lib.ps1"
$branch = (git -C $Repo rev-parse --abbrev-ref HEAD).Trim()
if ($branch -ne 'staging') { Write-Warning "You are on '$branch', not 'staging'. Work belongs on the staging branch." }

Write-Host '== build staging'
Invoke-Native npm @('run', 'build:staging') $Site | Out-Null
Write-Host '== checks'
Invoke-Native node @('release/checks.mjs', 'site-v2/dist-staging', 'staging') "$Repo\02_Website" | Out-Null
Write-Host '== deploy to iip-staging'
$out = Invoke-Native npx @('wrangler', 'pages', 'deploy', 'site-v2/dist-staging', '--project-name', 'iip-staging', '--branch', 'main', '--commit-dirty=true') "$Repo\02_Website"
$m = [regex]::Match($out, 'https://[a-z0-9]+\.iip-staging\.pages\.dev')
Write-Host '== smoke'
Invoke-Native node @('release/smoke.mjs', $StagingUrl, 'staging') "$Repo\02_Website" | Out-Null
$commit = (git -C $Repo rev-parse HEAD).Trim()
@{ commit = $commit; time = (Get-Date).ToUniversalTime().ToString('o'); deployment = $m.Value; smoke = 'PASS' } | ConvertTo-Json | Set-Content -Encoding utf8 "$Release\last-staging.json"
Write-Host "STAGING OK. This deployment: $($m.Value)"
Write-Host "Stable URL: $StagingUrl   Custom domain: https://staging.isapurindustrialpark.com (needs the cert to be active)"
