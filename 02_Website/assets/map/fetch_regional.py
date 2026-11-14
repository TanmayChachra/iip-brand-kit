"""Regional fetch for the home 'Where' map: motorway and trunk, big rivers, OSRM routes from the park. Cached in cache/. Run once."""
import json, pathlib, time, urllib.request, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import ovp
BB = (28.45, 77.15, 29.05, 77.95)
ovp.q("reg2_motor", 'way["highway"~"^(motorway|motorway_link|trunk)$"](BBOX);', BB)
PARK = (28.7826, 77.6560)
DEST = {"mod": (28.8320713, 77.5770873), "hap": (28.7299677, 77.775499), "meerut": (28.9845, 77.7064), "ghz": (28.6692, 77.4538),
        "delhi": (28.6469, 77.3155), "dadri": (28.5312, 77.5401), "ramp": (28.8013952, 77.6204507), "noida": (28.5708, 77.3261)}
for k, (la, lo) in DEST.items():
    f = ovp.C / f"osrm2_{k}.json"
    if f.exists(): continue
    u = f"https://router.project-osrm.org/route/v1/driving/{PARK[1]},{PARK[0]};{lo},{la}?overview=full&geometries=geojson"
    f.write_text(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "iip-website-map/1.0"}), timeout=60).read().decode(), encoding="utf-8"); time.sleep(1.5)
    d = json.loads(f.read_text()); print(k, d["routes"][0]["distance"] / 1000)

try:
    ovp.q("reg2_river", 'way["waterway"="river"]["name"~"Yamuna|Hindon"](BBOX);', BB)  # optional, map works without it
except SystemExit as ex:
    print("river skipped", ex)
