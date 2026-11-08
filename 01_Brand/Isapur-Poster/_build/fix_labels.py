"""Feature 3 -> Delhi-Meerut Expressway with distance, feature 4 -> Industrial Drainage."""
import re, pathlib
M = pathlib.Path(__file__).resolve().parents[1] / "03_Design/01_LATEST_isapur-industrial-park.svg"
s = M.read_text(encoding="utf-8")
t3 = re.search(r'<text id="feature-3".*?</text>', s, re.S).group(0)
n3 = re.sub(r"<tspan.*</tspan>", '<tspan x="0" y="0">Delhi-Meerut</tspan><tspan x="0" y="37">Expressway</tspan><tspan x="0" y="74" font-weight="500">4 km away</tspan>', t3, flags=re.S)
t4 = re.search(r'<text id="feature-4".*?</text>', s, re.S).group(0)
n4 = re.sub(r"<tspan.*</tspan>", '<tspan x="0" y="0">Waste Water</tspan><tspan x="0" y="37">Drainage</tspan>', t4, flags=re.S)
s = s.replace(t3, n3).replace(t4, n4)
M.write_text(s, encoding="utf-8")
print("ok")
