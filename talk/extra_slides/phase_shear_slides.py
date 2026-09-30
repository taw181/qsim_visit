"""Phase-shear readout: an extra slide, after the thank-you.

The same DeckSlide wrappers as the deck, imported from talk/aion_slides.py, so
it looks like the rest of it. It is in talk/deck.txt, after the HiFAIS slide,
as ``extra_slides/phase_shear_slides.py: PhaseShearReadoutSlide`` -- played and
rendered with the deck, but with no footer number. On its own, from the
project root:

    uv run manim-slides render -q l talk/extra_slides/phase_shear_slides.py PhaseShearReadoutSlide
    uv run manim-slides present PhaseShearReadoutSlide
"""

import sys
from pathlib import Path

from manim import *

# aion_slides.py is a script beside the package, not in it: put talk/ on the
# path to reach it. manim loads this file by path, so a relative import won't do.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aion_slides import Clicks  # noqa: E402
from aionanim.scenes.phase_shear import PhaseShearReadout  # noqa: E402


class PhaseShearReadoutSlide(Clicks, PhaseShearReadout):
    """A click once the square-on pulse and its atoms are up, once the ports
    are imaged; then the pulse tilts and the fringe period is marked."""

    CITE = ("sugarbakerEnhancedAtomInterferometer2013",)
