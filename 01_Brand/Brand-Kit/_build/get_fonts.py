import requests, pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

F = pathlib.Path(__file__).resolve().parents[1] / "fonts"
F.mkdir(exist_ok=True)
SRC = {
    "Montserrat-VF.ttf": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf",
    "Inter-VF.ttf": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
}
for n, u in SRC.items():
    p = F / n
    if not p.exists():
        r = requests.get(u, timeout=60); r.raise_for_status(); p.write_bytes(r.content)
    print(n, p.stat().st_size)

def inst(vf, out, axes):
    if (F / out).exists(): return
    f = TTFont(F / vf)
    g = instancer.instantiateVariableFont(f, axes)
    g.save(F / out)

inst("Montserrat-VF.ttf", "Montserrat-ExtraBold.ttf", {"wght": 800})
inst("Montserrat-VF.ttf", "Montserrat-SemiBold.ttf", {"wght": 600})
inst("Montserrat-VF.ttf", "Montserrat-Medium.ttf", {"wght": 500})
inst("Inter-VF.ttf", "Inter-Medium.ttf", {"wght": 500, "opsz": 14})
inst("Inter-VF.ttf", "Inter-SemiBold.ttf", {"wght": 600, "opsz": 14})
inst("Inter-VF.ttf", "Inter-Regular.ttf", {"wght": 400, "opsz": 14})
print(sorted(x.name for x in F.iterdir()))
