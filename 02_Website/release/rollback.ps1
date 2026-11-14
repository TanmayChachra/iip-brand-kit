# Roll production back. Needs the owner to type GO LIVE (same rule as promote.ps1).
# Quickest safe way (no build, instant): Cloudflare dashboard, Workers & Pages, iip-site, Deployments, pick the good one, "Rollback to this deployment".
# This script is the scripted way: it lists the last 5 production deployments, then rebuilds a previous release tag in a temp worktree and redeploys it.
# Usage: rollback.ps1 [-Tag prod-YYYYMMDD-HHMM] [-DryRun]   (no -Tag means the release before the newest one)
param([string]$Tag, [switch]$DryRun)
. "$PSScriptRoot\lib.ps1"
Write-Host '== last 5 production deployments'
$list = Invoke-Native npx @('wrangler', 'pages', 'deployment', 'list', '--project-name', 'iip-site', '--environment', 'production') "$Repo\02_Website"
$tags = @(git -C $Repo tag --list 'prod-*' --sort=-creatordate)
Write-Host "Release tags (newest first): $($tags[0..4] -join ', ')"
if (-not $Tag) { if ($tags.Count -lt 2) { Write-Host 'No previous release tag. Use the dashboard rollback.' -ForegroundColor Red; exit 1 }; $Tag = $tags[1] }
if ($tags -notcontains $Tag) { Write-Host "Unknown tag $Tag" -ForegroundColor Red; exit 1 }
$wt = Join-Path $env:TEMP "iip-rollback-$Tag"
if ($DryRun) { Write-Host "DRY RUN: would check out $Tag into $wt, build production, run checks, deploy to iip-site --branch main, smoke $ProdUrl. Nothing deployed."; exit 0 }
if ((Read-Host "Type GO LIVE to roll production back to $Tag") -ne 'GO LIVE') { Write-Host 'REFUSED: GO LIVE not typed' -ForegroundColor Red; exit 1 }
if (Test-Path $wt) { Invoke-Native git @('worktree', 'remove', '--force', $wt) | Out-Null }
Invoke-Native git @('worktree', 'add', '--detach', $wt, $Tag) | Out-Null
try {
  $wsite = "$wt\02_Website\site-v2"
  New-Item -ItemType Junction -Path "$wsite\node_modules" -Target "$Site\node_modules" | Out-Null
  Invoke-Native npm @('run', 'build:production') $wsite | Out-Null

  Invoke-Native npx @('wrangler', 'pages', 'deploy', 'site-v2/dist-production', '--project-name', 'iip-site', '--branch', 'main', '--commit-message', "rollback to $Tag") "$wt\02_Website" | Out-Null
  Start-Sleep -Seconds 5
  Invoke-Native node @('release/smoke.mjs', $ProdUrl, 'production') "$Repo\02_Website" | Out-Null
  "| $(Get-Date -Format 'yyyy-MM-dd HH:mm') | ROLLBACK | $Tag | | | smoke PASS |" | Add-Content -Encoding utf8 "$Release\RELEASES.md"
  Write-Host "ROLLED BACK to $Tag. main is now ahead of production: fix forward on staging, then promote."
} finally {
  cmd /c rmdir "$wsite\node_modules" 2>$null
  Invoke-Native git @('worktree', 'remove', '--force', $wt) | Out-Null
}
