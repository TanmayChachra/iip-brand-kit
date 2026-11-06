"""Full rebuild in the right order.  python Brand-Kit/_build/build_all.py   (then python Brand-Kit/_build/publish.py)"""
import subprocess, sys, pathlib
H = pathlib.Path(__file__).resolve().parent
for s in ("build_kit.py", "build_patterns2.py", "build_guides.py", "build_social.py", "build_signage.py", "build_stationery.py",
          "build_flatlay.py", "build_master.py", "export.py", "print_colors.py"):
    print("==", s, flush=True)
    subprocess.run([sys.executable, str(H / s)], check=True)
