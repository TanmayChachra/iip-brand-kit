# One command: powershell -File 02_Website/previews/deploy.ps1
# Needs `npx wrangler login` once (browser) or CLOUDFLARE_API_TOKEN set by the owner. Never put a token in this file.
$ErrorActionPreference = 'Stop'
# GUARD: this script deploys previews only (iipreview-*). Production is iip-site and only 02_Website/release/promote.ps1 may touch it.
if ($args -match 'iip-site' -or $env:PROJECT -eq 'iip-site') { throw 'refusing to target iip-site' }
$here = $PSScriptRoot
Push-Location "$here\..\site-v2"
npm run build
Pop-Location
Push-Location "$here\..\site"
npm run build
Pop-Location
node "$here\package.mjs"
$rows = @()
foreach ($p in 'nav','v3','v1','kit') {
  if ("iipreview-$p" -match 'iip-site|iip-staging') { throw 'previews must never target iip-site' }
  $out = npx wrangler pages deploy "$here\dist\$p" --project-name "iipreview-$p" --branch main --commit-dirty=true 2>&1 | Out-String
  $m = [regex]::Match($out, 'https://[a-z0-9]+\.iipreview-' + $p + '\.pages\.dev')
  $url = "https://iipreview-$p.pages.dev/"
  try { $r = Invoke-WebRequest -Uri $url -UseBasicParsing; $code = $r.StatusCode; $xr = $r.Headers['X-Robots-Tag'] } catch { $code = 'ERR'; $xr = '' }
  Write-Host "$p -> $url ($code, $xr) deployment $($m.Value)"
  $rows += "| $p | $url | $($m.Value) | $code | $xr |"
}
$date = Get-Date -Format 'yyyy-MM-dd HH:mm'
@("# Preview links (private, noindex)", "", "Deployed $date. Start at https://iipreview-nav.pages.dev/", "", "| Folder | URL | This deployment | HTTP | X-Robots-Tag |", "|---|---|---|---|---|") + $rows | Set-Content -Encoding utf8 "$here\LINKS.md"
