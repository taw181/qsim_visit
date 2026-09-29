"""The bare black-hole merger: out of the talk, kept as an extra slide.

The same DeckSlide wrapper as the deck, imported from talk/aion_slides.py, so
it looks like the rest of it; it is not in talk/deck.txt, so it carries no
footer number. Render and present it by name, from the project root:

    uv run manim-slides render -q l talk/extra_slides/black_hole_merger_slides.py \
        BlackHoleMergerSlide
    uv run manim-slides present BlackHoleMergerSlide
"""

import sys
from pathlib import Path

from manim import *

# aion_slides.py is a script beside the package, not in it: put talk/ on the
# path to reach it. manim loads this file by path, so a relative import won't do.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aion_slides import DeckSlide  # noqa: E402
from aionanim.scenes.gravitational_waves import BlackHoleMerger  # noqa: E402


class BlackHoleMergerSlide(DeckSlide, BlackHoleMerger):
    """No stops: the merger plays straight through from the moment the slide
    comes up, and holds on the settled sheet as the slide's own end."""
