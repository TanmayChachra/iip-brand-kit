# Cuts static Montserrat instances from the official variable font (OFL), so apps without variable-font support still work.
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont, OverlapMode
from fontTools.varLib import instancer
src, outdir = sys.argv[1], sys.argv[2]
for name, w in [("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800), ("Black", 900)]:
    f = TTFont(src)
    f = instantiateVariableFont(f, {"wght": w}, updateFontNames=True)
    f.save(f"{outdir}/Montserrat-{name}.ttf")
    n = f["name"]; print(name, n.getDebugName(1), "|", n.getDebugName(2), "|", n.getDebugName(4))
