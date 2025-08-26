from __future__ import annotations
import time
from datetime import datetime
from typing import Tuple, Dict
import numpy as np
from PIL import Image
import mss
import hashlib
from schemas import ScreenshotMeta

def dhash(image: Image.Image, hash_size: int = 8) -> str:
    # Perceptual difference hash
    image = image.convert("L").resize((hash_size + 1, hash_size), Image.LANCZOS)
    diff = np.array(image)[:, 1:] > np.array(image)[:, :-1]
    return "%0*x" % (hash_size * hash_size // 4, int("".join("1" if v else "0" for v in diff.flatten()), 2))

def capture_region(region: Dict[str, int]) -> Tuple[Image.Image, ScreenshotMeta]:
    with mss.mss() as sct:
        bbox = {"left": region["x"], "top": region["y"], "width": region["width"], "height": region["height"]}
        raw = sct.grab(bbox)
        img = Image.frombytes("RGB", raw.size, raw.rgb)
        h = dhash(img, 16)
        meta = ScreenshotMeta(
            path="",  # set by caller when saved
            timestamp=datetime.utcnow(),
            hash=h,
            width=img.width,
            height=img.height,
        )
        return img, meta

def save_image(img: Image.Image, folder: str, prefix: str = "shot") -> str:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    path = f"{folder}/{prefix}_{ts}.png"
    img.save(path)
    return path
