"""Build the phone-friendly web player for the rendered deck.

Reads talk/deck.txt and each slide's manim-slides config in slides/, copies
every segment's video (remuxed with faststart so it streams) into OUT/v/, and
writes OUT/index.html with the deck inlined as a manifest. The work is
manim_atoms.slides.player's; this file says how the talk's menu reads.

    talk/deck.sh render m
    talk/deck.sh player [OUT]     # default: player/
"""

import os
import sys
from pathlib import Path

from manim_atoms.slides.deck import load_deck
from manim_atoms.slides.player import build_player

ROOT = Path(__file__).resolve().parent.parent

# The sections as the outline numbers them; a slide belongs to the last
# section slide before it.
SECTION_SLIDES = {
    "AtomInterferometrySlide": "1 · Atom interferometry",
    "MotivationSlide": "2 · Motivation",
    "PrototypeDeviceSlide": "3 · Our prototype device",
    "FuturePlansSlide": "4 · Future plans",
    "OutroSlide": "Outro",
}
# Names for the menu where the class name reads badly once split.
NAMES = {
    "TitleSlide": "Title",
    "SinglePhotonMachZehnderSlide": "Single-photon Mach-Zehnder",
    "ClockPhaseTermsSlide": "The interferometer is a clock",
    "LaserNoiseLissajousSlide": "Laser noise and the Lissajous ellipse",
    "ContentsSlide": "Outline",
    "AIONCollabSlide": "The AION collaboration",
    "AIONChambersSlide": "AION chambers across the UK",
    "Aion10BeecroftSlide": "AION-10 at Oxford",
    "AICECernSlide": "AICE at CERN",
    "LMTMachZehnderSlide": "LMT Mach-Zehnder",
    "LMTResultsSlide": "LMT results",
    "GradiometerGWStretchSlide": "Gradiometer: a stretching baseline",
    "DarkMatterGradiometerSlide": "Dark matter, measured differentially",
    "OutroSlide": "Thank you",
}


def main(argv=()):
    os.chdir(ROOT)  # slides/ and its videos are found from the project root
    out = Path(argv[0]) if argv else ROOT / "player"
    build_player(load_deck(ROOT / "talk" / "deck.txt"), out, sections=SECTION_SLIDES,
                 names=NAMES, title="Freiburg AION Talk")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
