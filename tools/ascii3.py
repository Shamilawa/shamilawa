import sys, json
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw

from pathlib import Path

SRC = Path(__file__).with_name("avatar.png")
CROP = (135, 5, 345, 265)   # head + shoulders out of the 460x460 avatar

RAMPS = {
    "classic": "@%#*+=-:. ",
    "soft":    "@&%#*+=~-:.  ",
    "mini":    "@#*+=:. ",
}


def subject_mask(img, tol=52):
    """Flood fill inward from the top/side borders to knock out the bright wall."""
    work = img.filter(ImageFilter.GaussianBlur(2)).convert("L")
    w, h = work.size
    flood = work.copy()
    seeds = []
    for x in range(0, w, 6):
        seeds.append((x, 0))
        seeds.append((x, 1))
    for y in range(0, int(h * 0.55), 6):
        seeds.append((0, y))
        seeds.append((w - 1, y))
    for s in seeds:
        if flood.getpixel(s) > 110:
            ImageDraw.floodfill(flood, s, 255, thresh=tol)
    # anything driven to pure white by the fill is background
    mask = flood.point(lambda v: 0 if v >= 254 else 255)
    return mask.filter(ImageFilter.MedianFilter(5))


def build(width=48, ramp_name="classic", contrast=1.55, gamma=0.9,
          aspect=0.5, tol=52, local=1.0, invert=False):
    src = Image.open(SRC).crop(CROP)
    mask = subject_mask(src, tol)

    g = src.convert("L").filter(ImageFilter.UnsharpMask(radius=3, percent=130, threshold=2))
    g = ImageOps.autocontrast(g, cutoff=1)
    if local != 1.0:
        # lift midtones so the face isn't a hollow void
        g = g.point(lambda v: min(255, int((v / 255) ** local * 255)))
    g = ImageEnhance.Contrast(g).enhance(contrast)

    w, h = src.size
    height = max(1, round(width * (h / w) * aspect))
    g = g.resize((width, height), Image.LANCZOS)
    m = mask.resize((width, height), Image.LANCZOS)

    ramp = RAMPS[ramp_name]
    n = len(ramp) - 1
    gp, mp = g.load(), m.load()
    out = []
    for y in range(height):
        row = []
        for x in range(width):
            if mp[x, y] < 110:
                row.append(" ")
                continue
            v = (gp[x, y] / 255) ** gamma
            if invert:
                v = 1.0 - v
            row.append(ramp[int(v * n + 0.5)])
        out.append("".join(row).rstrip())
    return out


if __name__ == "__main__":
    cfg = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    for line in build(**cfg):
        print(line)
