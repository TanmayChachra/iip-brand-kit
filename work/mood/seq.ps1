$R='D:\SILVERLEAF_BUILDCON\03_Marketing\IIP Branding'
foreach($n in 'r1-quiet','r4-heritage','r6-owned-colour','r8-editorial'){
 $l=if($n -eq 'r8-editorial'){"$R\References\inspiration-ads\markefy-red-stairs-we-build-the-next-step.png"}else{"$R\References\iterations-chatgpt\B-white-minimal\identity-board.png"}
 & powershell -NoProfile -File "$R\work\gen\cx.ps1" "$R\work\mood\p-$n.txt" "$R\work\mood\$n.log" "$R\work\logo\iip-master-1x.png" $l
}
