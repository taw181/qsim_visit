"""Spin squeezing by a cavity measurement: an extra slide, at the end.

The same DeckSlide wrappers as the deck, imported from talk/aion_slides.py, so
it looks like the rest of it. It is in talk/deck.txt, last, as
``extra_slides/squeezing_slides.py: SpinSqueezingSlide`` -- played and
rendered with the deck, but with no footer number. On its own, from the
project root:

    uv run manim-slides render -q l talk/extra_slides/squeezing_slides.py SpinSqueezingSlide
    uv run manim-slides present SpinSqueezingSlide
"""

import sys
from pathlib import Path

from manim import *

# aion_slides.py is a script beside the package, not in it: put talk/ on the
# path to reach it. manim loads this file by path, so a relative import won't do.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aion_slides import Clicks  # noqa: E402
from manim_atoms.interferometry.scenes.squeezing import SpinSqueezing  # noqa: E402


class SpinSqueezingSlide(Clicks, SpinSqueezing):
    """A click once the coherent state is up, once the cavity has read out
    N_g, once the disc is squeezed; then it turns onto the phase."""

    CITE = (
        "chenConditionalSpinSqueezing2011",
        "hostenMeasurementNoise1002016",
        "greveEntanglementenhancedMatterwaveInterferometry2022",
    )
