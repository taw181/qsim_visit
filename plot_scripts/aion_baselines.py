"""Write the AION baseline sketches to ``figures/``: AION-km's,
``aion_km_baseline.png``, and AION-10's, ``aion_10_baseline.png``.

Stills of manim_atoms.aion.tools.baseline's drawing -- four interferometers along a
1 km shaft, and two along 10 m -- on a transparent background, cropped to the
drawing, for a slide to place as a picture. Drawn on the deck's own frame and
only then cropped, since manim scales stroke widths with the frame: placed at
the shaft's length in scene units tall, each matches the slides' line weights.

    .venv/bin/python plot_scripts/aion_baselines.py
"""

from pathlib import Path

import numpy as np
from manim import Camera, tempconfig

from manim_atoms.aion.tools.baseline import make_baseline

ROOT = Path(__file__).resolve().parent.parent
# file name: (the shaft's length in scene units, which the slide places it
# at; interferometers along it; the baseline's label)
SKETCHES = {
    "aion_km_baseline.png": (5.6, 4, r"1\,\mathrm{km}"),
    "aion_10_baseline.png": (5.2, 2, r"10\,\mathrm{m}"),
}
MARGIN_PX = 12


def draw(out, height, n, label):
    sketch = make_baseline(-height / 2, height / 2, n=n, label=label)
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
    out.parent.mkdir(exist_ok=True)
    image.save(out)
    print(f"wrote figures/{out.name}, {image.size[0]} x {image.size[1]} px")


def main():
    for name, (height, n, label) in SKETCHES.items():
        draw(ROOT / "figures" / name, height, n, label)


if __name__ == "__main__":
    main()
