# usage: powershell -File cx.ps1 <promptfile> <logfile> [image1 image2 ...]
param([string]$Prompt, [string]$Log, [string[]]$Images)
$codex = "C:\Users\anshc\AppData\Local\OpenAI\Codex\bin\22cfb1d302613eae\codex.exe"
$args2 = @('exec', '--skip-git-repo-check', '-s', 'workspace-write', '-C', 'D:\SILVERLEAF_BUILDCON\03_Marketing\IIP Branding')
foreach ($i in $Images) { if ($i) { $args2 += @('-i', $i) } }
$args2 += '-'
Get-Content -Raw $Prompt | & $codex @args2 *> $Log
