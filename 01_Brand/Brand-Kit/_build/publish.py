"""Rebuild everything and copy to docs/ (GitHub Pages).  python 01_Brand/Brand-Kit/_build/publish.py"""
import subprocess, sys, shutil, pathlib
H = pathlib.Path(__file__).resolve().parent; BRAND = H.parents[1]; ROOT = H.parents[2]   # ROOT = repo root, BRAND = 01_Brand
for s in ("build_site.py", "build_book.py", "build_brief.py"): subprocess.run([sys.executable, str(H / s)], check=True)
D = ROOT / "docs"; D.mkdir(exist_ok=True)
for c in D.iterdir():
    if c.name not in (".nojekyll", "CNAME", "experiments", "board"): shutil.rmtree(c) if c.is_dir() else c.unlink()
shutil.copytree(BRAND / "Brand-Kit/site", D, dirs_exist_ok=True); (D / ".nojekyll").touch()
print("published to docs/")
