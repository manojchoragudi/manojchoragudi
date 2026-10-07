"""Run once per photo: python scripts/prep_photo.py my-photo.jpg  ->  scripts/photo-prepped.png
Boosts local contrast (CLAHE) so a flatly-lit face keeps highlights and shadows.
If `rembg` is installed it also removes the background (subject on black)."""
import sys

import cv2
import numpy as np
from PIL import Image

src = sys.argv[1] if len(sys.argv) > 1 else "scripts/photo.jpg"
img = Image.open(src).convert("RGB")
alpha = None
try:
    from rembg import remove
    cut = remove(img)
    alpha = np.array(cut.split()[-1]) / 255.0
except ImportError:
    print("rembg not installed - skipping background removal")

gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(gray)
if alpha is not None:
    gray = (gray * alpha).astype("uint8")  # background -> black -> blank in ASCII
Image.fromarray(gray).save("scripts/photo-prepped.png")
print("wrote scripts/photo-prepped.png")
