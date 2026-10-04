#!/usr/bin/env bash
# The Freiburg talk: render, present or convert the deck in talk/aion_slides.py.
#
#   talk/deck.sh render [-j N] [-f FPS] [l|m|h] [Slide ...]   # default h; all slides, or just those named;
#                                                     # -j N renders N slides at once (logs in media/deck_logs/);
#                                                     # -f FPS frame rate, default 30 (l keeps its 15)
#   talk/deck.sh present
#   talk/deck.sh html                         # aion_talk.html, one standalone file
#   talk/deck.sh player [OUT]                 # the web player (default player/), after render
#
# Run from anywhere; it works from the project root so manim.cfg applies.
# The deck's order lives in talk/deck.txt, shared with deck.py (the no-bash
# twin); the work is manim_atoms' manim-atoms-deck.
set -euo pipefail
cd "$(dirname "$0")/.."

case "${1:-}" in
    render | present | html)
        exec uv run manim-atoms-deck --deck talk/deck.txt --slides talk/aion_slides.py \
            --html aion_talk.html "$@"
        ;;
    player)
        shift
        exec uv run python talk/build_player.py "$@"
        ;;
    *)
        sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
        exit 1
        ;;
esac
