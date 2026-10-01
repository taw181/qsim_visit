"""Write the AION-km baseline sketch to ``figures/aion_km_baseline.png``.

A still of aionanim.tools.baseline's drawing -- four interferometers along a
1 km shaft -- on a transparent background, cropped to the drawing, for a
slide to place as a picture. Drawn on the deck's own frame and only then
cropped, since manim scales stroke widths with the frame: placed at
``HEIGHT`` scene units tall, it matches the slides' line weights.

    .venv/bin/python plot_scripts/aion_km_baseline.py
"""

from pathlib import Path

import numpy as np
from manim import Camera, tempconfig

from aionanim.tools.baseline import make_baseline

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "figures" / "aion_km_baseline.png"
HEIGHT = 5.6  # the shaft's length, in scene units: the slide places it at this
MARGIN_PX = 12


def main():
    sketch = make_baseline(-HEIGHT / 2, HEIGHT / 2, n=4)
    sketch.move_to([0, 0, 0])
    with tempconfig({
        "pixel_width": 3840, "pixel_height": 2160, "background_opacity": 0.0,
    }):
        camera = Camera()
        camera.capture_mobject(sketch)
        image = camera.get_image()
    alpha = np.asarray(image)[..., 3]
    rows, cols = np.nonzero(alpha)
    image = image.crop((
        max(cols.min() - MARGIN_PX, 0), max(rows.min() - MARGIN_PX, 0),
        cols.max() + MARGIN_PX + 1, rows.max() + MARGIN_PX + 1,
    ))
    OUT.parent.mkdir(exist_ok=True)
    image.save(OUT)
    print(f"wrote figures/{OUT.name}, {image.size[0]} x {image.size[1]} px")


if __name__ == "__main__":
    main()
