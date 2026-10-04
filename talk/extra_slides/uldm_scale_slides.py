"""The ULDM wave flown out across the solar system: an extra slide, out of the deck.

DarkMatterScale zooms from the Earth out to the Sun with the wave laid over
them. The deck shows the same three masses on the full-size plot instead
(DarkMatterScaleSlide); this is kept to be played by name, or put back in
talk/deck.txt as ``extra_slides/uldm_scale_slides.py: DarkMatterScaleFlyoutSlide``.
From the project root:

    uv run manim-slides render -q l talk/extra_slides/uldm_scale_slides.py DarkMatterScaleFlyoutSlide
    uv run manim-slides present DarkMatterScaleFlyoutSlide
"""

import sys
from pathlib import Path

from manim import *

# aion_slides.py is a script beside the package, not in it: put talk/ on the
# path to reach it. manim loads this file by path, so a relative import won't do.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aion_slides import RunsOnIntoLoops  # noqa: E402
from manim_atoms.bibliography import AUTHOR_YEAR  # noqa: E402
from manim_atoms.aion.scenes.uldm_scale import DarkMatterScale  # noqa: E402


class DarkMatterScaleFlyoutSlide(RunsOnIntoLoops, DarkMatterScale):
    CITE = ("badurinaAIONAtomInterferometer2020",)  # the inset's curves
    # short, to end before the Earth's limb in the first view and clear the
    # verdict in the last
    CITE_FORMAT = AUTHOR_YEAR

    def hold(self):
        self.loop(super().hold)
