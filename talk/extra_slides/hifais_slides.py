"""HiFAIS, our high-flux Sr source: an extra slide, after the thank-you.

The same DeckSlide wrappers as the deck, imported from talk/aion_slides.py, so
it looks like the rest of it. It is in talk/deck.txt, after OutroSlide, as
``extra_slides/hifais_slides.py: HighFluxLoadingSlide`` -- a slide named with
its file is played and rendered with the deck but takes no footer number and
no place on the contents page. On its own, from the project root:

    uv run manim-slides render -q l talk/extra_slides/hifais_slides.py HighFluxLoadingSlide
    uv run manim-slides present HighFluxLoadingSlide
"""

import sys
from pathlib import Path

from manim import *

# aion_slides.py is a script beside the package, not in it: put talk/ on the
# path to reach it. manim loads this file by path, so a relative import won't do.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aion_slides import Clicks  # noqa: E402
from aionanim.scenes.hifais import HighFluxLoading  # noqa: E402


class HighFluxLoadingSlide(Clicks, HighFluxLoading):
    """A click once the chamber is up, once the source is running beside the
    empty plot, and once the MOT has loaded; then the loading rate."""

    CITE = ("walkerHighfluxSourceCold2026",)
