"""Render LIGO during the merger and ship the video with the package.

MergerOnSensitivityPlot plays LIGODuringMerger (the LIGO Michelson, set up
from the first frame and driven by the merger's own chirp) beside the
merger's first run, as a recorded video rather than as live mobjects: the
scene is laid out for the full frame, and its always_redraw beams can't be
shrunk into half of it. This renders ``aionanim/scenes/ligo.py``'s
``LIGODuringMerger`` at -qh and copies the result to
``src/aionanim/data/videos/ligo_michelson.mp4``, which is what
``aionanim.scenes.gravitational_waves`` reads. Re-run it after changing
either scene's timing or the LIGO drawing.

    .venv/bin/python data_scripts/render_ligo_michelson.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENE_FILE = ROOT / "src" / "aionanim" / "scenes" / "ligo.py"
RENDERED = ROOT / "media" / "videos" / "ligo" / "1080p60" / "LIGODuringMerger.mp4"
OUT = ROOT / "src" / "aionanim" / "data" / "videos" / "ligo_michelson.mp4"


def main():
    # From the project root, so manim.cfg (background colour, media dir) applies.
    subprocess.run(
        [sys.executable, "-m", "manim", "-qh", str(SCENE_FILE), "LIGODuringMerger"],
        cwd=ROOT, check=True,
    )
    shutil.copyfile(RENDERED, OUT)
    print(f"{RENDERED} -> {OUT}")


if __name__ == "__main__":
    main()
