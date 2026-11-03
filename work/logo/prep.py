"""Clean transparent masters from the supplied logo.jpeg. Logo artwork is untouched: only the white
page, the faint die-cut outline and the '1/1' screenshot marker are removed."""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi

src = "IIP Assets/logo.jpeg"
im = np.array(Image.open(src).convert("RGB")).astype(np.int32)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
# artwork = yellow, red, green, or dark outline. Near-white / light grey = background.
mx, mn = im.max(2), im.min(2)
sat = mx - mn
art = (sat > 60) | (mx < 110)
art = ndi.binary_closing(art, iterations=2)
art = ndi.binary_fill_holes(art)
lab, n = ndi.label(art)
sizes = ndi.sum(art, lab, range(1, n + 1))
art = lab == (1 + int(np.argmax(sizes)))
ys, xs = np.where(art)
y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
print("bbox", x0, y0, x1, y1)
pad = 6
crop = im[y0 - pad:y1 + pad + 1, x0 - pad:x1 + pad + 1].astype(np.uint8)
m = art[y0 - pad:y1 + pad + 1, x0 - pad:x1 + pad + 1].astype(np.uint8) * 255
# smooth matte edge
m = cv2.GaussianBlur(m, (0, 0), 0.8)
rgba = np.dstack([crop, m])
out = Image.fromarray(rgba, "RGBA")
side = max(out.size)
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(out, ((side - out.width) // 2, (side - out.height) // 2))
canvas.save("work/logo/iip-master-1x.png")
big = canvas.resize((side * 3, side * 3), Image.LANCZOS)
big.save("work/logo/iip-master-3x.png")
print("saved", canvas.size, big.size)
