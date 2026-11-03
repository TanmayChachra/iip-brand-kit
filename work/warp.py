"""Warp exact artwork into the blank white panel of a scene photo, keeping the panel's own light, seams and dirt."""
import sys, pathlib, numpy as np, cv2
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "mock"; OUT.mkdir(exist_ok=True)


def find_quad(img, hint=None):
    """largest bright, low-saturation blob -> 4 corners (tl, tr, br, bl)."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 2] > 150) & (hsv[..., 1] < 45)).astype(np.uint8) * 255
    if hint is not None:  # restrict to a rough (x0,y0,x1,y1) window
        w = np.zeros_like(m); x0, y0, x1, y1 = hint; w[y0:y1, x0:x1] = 255; m &= w
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea)
    hull = cv2.convexHull(c)
    eps = 0.01 * cv2.arcLength(hull, True)
    q = cv2.approxPolyDP(hull, eps, True).reshape(-1, 2).astype(np.float32)
    while len(q) > 4:
        eps *= 1.3; q = cv2.approxPolyDP(hull, eps, True).reshape(-1, 2).astype(np.float32)
    if len(q) < 4:
        r = cv2.minAreaRect(hull); q = cv2.boxPoints(r).astype(np.float32)
    s = q.sum(1); d = (q[:, 0] - q[:, 1])
    tl, br = q[np.argmin(s)], q[np.argmax(s)]
    tr, bl = q[np.argmax(d)], q[np.argmin(d)]
    return np.array([tl, tr, br, bl], np.float32)


def composite(scene_path, art_path, out_path, inset=0.012, hint=None, quad=None):
    sc = cv2.imread(str(scene_path)); art = cv2.imread(str(art_path))
    quad = find_quad(sc, hint) if quad is None else np.array(quad, np.float32)
    c = quad.mean(0); quad = c + (quad - c) * (1 - inset)  # keep clear of the frame
    h, w = art.shape[:2]
    M = cv2.getPerspectiveTransform(np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32), quad)
    warped = cv2.warpPerspective(art, M, (sc.shape[1], sc.shape[0]), flags=cv2.INTER_AREA)
    mask = cv2.warpPerspective(np.full((h, w), 255, np.uint8), M, (sc.shape[1], sc.shape[0]))
    mask = cv2.GaussianBlur(mask, (0, 0), 0.8).astype(np.float32)[..., None] / 255
    # panel shading: luminance of the blank panel, normalised, re-applied to the artwork (multiply)
    g = cv2.cvtColor(sc, cv2.COLOR_BGR2GRAY).astype(np.float32)
    pm = mask[..., 0] > 0.99
    ref = np.percentile(g[pm], 92)
    shade = np.clip(g / ref, 0.55, 1.05)[..., None]
    shade = cv2.GaussianBlur(shade, (0, 0), 1.2)[..., None] if shade.ndim == 2 else shade
    lit = warped.astype(np.float32) * (0.35 + 0.65 * shade)
    # match the photo: slight softness + grain
    lit = cv2.GaussianBlur(lit, (0, 0), 0.7)
    lit += np.random.default_rng(3).normal(0, 2.2, lit.shape)
    outimg = sc.astype(np.float32) * (1 - mask) + lit * mask
    cv2.imwrite(str(out_path), np.clip(outimg, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
    return quad


if __name__ == "__main__":
    scene = ROOT / sys.argv[1]; tag = sys.argv[2]; kind = sys.argv[3]
    for kit in ["jamun", "gulaal", "kora"]:
        q = composite(scene, ROOT / f"wide/{kit}-{kind}.png", OUT / f"{kit}-{tag}.jpg", quad=(__import__("json").loads(sys.argv[4]) if len(sys.argv) > 4 else None))
    print(q.tolist())

