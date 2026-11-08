"""Worked example of adapting the kit: change ONLY content.json values, rebuild, get new on-brand assets.
Writes examples/ and restores content.json afterwards."""
import json, pathlib, shutil, subprocess, sys
KIT = pathlib.Path(__file__).resolve().parents[1]
CJ = KIT / "tokens/content.json"
orig = CJ.read_text(encoding="utf-8")
EX = KIT / "examples"; EX.mkdir(exist_ok=True)
VARIANTS = {
    "A-proof-lines-on": {"show_proof": True},
    "B-new-line-plots-available": {"tagline": ["Industrial", "Plots", "Available."], "tagline_one_line": "Industrial Plots Available.", "show_proof": True},
}
try:
    for name, patch in VARIANTS.items():
        d = json.loads(orig); d.update(patch); CJ.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
        subprocess.run([sys.executable, str(KIT / "_build/build_kit.py")], check=True)
        for t in ("pole-board-20x32in-photo", "hoarding-40x15ft", "street-pole-24x36in-2to3"):
            shutil.copy(KIT / "outlined/04_Templates" / f"{t}.svg", EX / f"{name}__{t}.svg")
finally:
    CJ.write_text(orig, encoding="utf-8")
    subprocess.run([sys.executable, str(KIT / "_build/build_kit.py")], check=True)
print(sorted(p.name for p in EX.iterdir()))
