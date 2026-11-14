# Shared helpers, dot-sourced by the release scripts. Holds no secrets: wrangler uses the owner's `wrangler login`.
$ErrorActionPreference = 'Stop'
$script:Release = $PSScriptRoot
$script:Site = (Resolve-Path "$PSScriptRoot\..\site-v2").Path
$script:Repo = (Resolve-Path "$PSScriptRoot\..\..").Path
$env:CLOUDFLARE_ACCOUNT_ID = '93883b0f1a665f2471bf039ae10d748c'   # IsapurIndustrialPark account id (not a secret), this process only
$script:StagingUrl = 'https://iip-staging.pages.dev'
$script:ProdUrl = 'https://isapurindustrialpark.com'

# Run a native command, stream its output, return the text, throw on a non-zero exit code.
function Invoke-Native([string]$Exe, [string[]]$Arguments, [string]$Dir = $script:Repo) {
  Push-Location $Dir
  $prev = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
  try {
    $out = & $Exe @Arguments 2>&1 | ForEach-Object { "$_" } | Out-String
    $code = $LASTEXITCODE
  } finally { $ErrorActionPreference = $prev; Pop-Location }
  Write-Host $out.TrimEnd()
  if ($code -ne 0) { throw "$Exe $($Arguments -join ' ') failed with exit code $code" }
  return $out
}
function Get-Git([string[]]$Arguments) { (Invoke-Native git $Arguments | Out-String).Trim() }
function Get-ChecksJson { Get-Content "$script:Release\last-checks.json" -Raw | ConvertFrom-Json }
