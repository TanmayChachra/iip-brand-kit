"""Concept route mockups: steps ad on the hoarding and on the street-pole row."""
import shutil
import warp as W
import mock2 as M

R = M.ROOT
C = R / "concept"
O = M.OUT
W.composite(R / "gen/scene-hoarding-a.png", C / "steps-hoarding.png", O / "concept-steps-hoarding.jpg", quad=M.HOARD)
cur = R / "gen/scene-poles-a.png"
for i, q in enumerate(M.ROW):
    tmp = O / "_c-row.jpg"
    W.composite(cur, C / "steps-tall.png", tmp, quad=q, inset=0.0)
    cur = O / f"_c-row{i}.jpg"; shutil.copy(tmp, cur)
shutil.copy(cur, O / "concept-steps-row.jpg")
print("ok")
