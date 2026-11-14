"""Polite Overpass fetch with cache. usage: ovp.py name 'query'"""
import sys, json, pathlib, time, urllib.request, urllib.parse
C = pathlib.Path(__file__).parent / "cache"
def q(name, body, bbox):
    f = C / f"{name}.json"
    if f.exists(): return json.loads(f.read_text(encoding="utf-8"))
    s, w, n, e = bbox
    ql = f"[out:json][timeout:60];({body.replace('BBOX', f'{s},{w},{n},{e}')});out geom;"
    EPS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter", "https://overpass.private.coffee/api/interpreter"]
    req = urllib.request.Request(EPS[0], data=urllib.parse.urlencode({"data": ql}).encode(), headers={"User-Agent": "iip-website-map/1.0 (static map artwork, few requests)"})
    for i in range(6):
        req.full_url = EPS[i % len(EPS)]
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=90).read()); break
        except Exception as ex:
            print("retry", name, ex); time.sleep(10)
    else: raise SystemExit("overpass failed " + name)
    f.write_text(json.dumps(d), encoding="utf-8"); time.sleep(3); return d
