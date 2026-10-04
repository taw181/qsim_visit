"""The Freiburg talk, without bash (Windows): render, present or convert the deck.

    uv run talk/deck.py render [-j N] [-f FPS] [l|m|h] [Slide ...]   # default h; all slides, or just those named;
                                                            # -j N renders N slides at once (logs in media/deck_logs/);
                                                            # -f FPS frame rate, default 30 (l keeps its 15)
    uv run talk/deck.py present
    uv run talk/deck.py html                                # aion_talk.html, one standalone file
    uv run talk/deck.py player [OUT]                        # the web player (default player/), after render

The same commands as deck.sh, and the same deck order (talk/deck.txt); the
work is manim_atoms' manim-atoms-deck. Run from anywhere, it works from the
project root so manim.cfg applies.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    os.chdir(ROOT)
    if sys.argv[1:2] == ["player"]:
        sys.path.insert(0, str(ROOT / "talk"))
        from build_player import main as player

        return player(sys.argv[2:])
    from manim_atoms.slides.cli import main as deck

    return deck(["--deck", "talk/deck.txt", "--slides", "talk/aion_slides.py",
                 "--html", "aion_talk.html", *sys.argv[1:]])


if __name__ == "__main__":
    sys.exit(main())
