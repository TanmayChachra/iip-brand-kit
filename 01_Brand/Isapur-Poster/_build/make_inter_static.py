# Cuts static Inter instances (opsz 14) from the official variable font (OFL).
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
src, outdir = sys.argv[1], sys.argv[2]
for name, w in [("Regular", 400), ("Medium", 500), ("SemiBold", 600)]:
    f = instantiateVariableFont(TTFont(src), {"wght": w, "opsz": 14}, updateFontNames=True)
    f.save(f"{outdir}/Inter-{name}.ttf")
    n = f["name"]; print(name, "|", n.getDebugName(1), "|", n.getDebugName(2), "|", n.getDebugName(4))
