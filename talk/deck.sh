#!/usr/bin/env bash
# The Freiburg talk: render, present or convert the deck in talk/aion_slides.py.
#
#   talk/deck.sh render [-j N] [-f FPS] [l|m|h] [Slide ...]   # default h; all slides, or just those named;
#                                                     # -j N renders N slides at once (logs in media/deck_logs/);
#                                                     # -f FPS frame rate, default 30 (l keeps its 15)
#   talk/deck.sh present
#   talk/deck.sh html                         # aion_talk.html, one standalone file
#
# Run from anywhere; it works from the project root so manim.cfg applies.
set -euo pipefail
cd "$(dirname "$0")/.."

# The deck's order lives in talk/deck.txt, shared with deck.py (the no-bash twin).
mapfile -t DECK < <(sed -e 's/#.*//' -e 's/[[:space:]]//g' -e '/^$/d' talk/deck.txt)

case "${1:-}" in
    render)
        shift
        jobs=1
        fps=
        while [[ "${1:-}" == -[jf]* ]]; do
            opt="${1:0:2}"
            val="${1:2}"
            shift
            [[ -n "$val" ]] || { val="${1:?$opt needs a number}"; shift; }
            case "$opt" in -j) jobs="$val" ;; -f) fps="$val" ;; esac
        done
        quality=h
        if [[ "${1:-}" =~ ^[lmhpk]$ ]]; then
            quality="$1"
            shift
        fi
        # 30 fps unless asked otherwise: slide animations don't need 60, and
        # it halves the frames at h. l keeps its own 15.
        [[ -n "$fps" ]] || { [[ "$quality" == l ]] && fps=15 || fps=30; }
        (( $# )) || set -- "${DECK[@]}"
        # -q h, not -qh: manim-slides reads the h of -qh as --help.
        if (( jobs == 1 )); then
            uv run manim-slides render -q "$quality" --fps "$fps" talk/aion_slides.py "$@"
            exit
        fi
        # Cairo renders on one core, so run one process per slide, each
        # logging to media/deck_logs/<Slide>.log rather than interleaving.
        mkdir -p media/deck_logs
        uv sync -q
        render_one() {
            local log="media/deck_logs/$1.log"
            if uv run --no-sync manim-slides render -q "$2" --fps "$3" talk/aion_slides.py "$1" >"$log" 2>&1; then
                echo "done    $1"
            else
                echo "FAILED  $1  (see $log)"
                return 1
            fi
        }
        export -f render_one
        printf '%s\n' "$@" | xargs -P "$jobs" -I{} bash -c 'render_one "$1" "$2" "$3"' _ {} "$quality" "$fps"
        ;;
    present)
        uv run manim-slides present "${DECK[@]}"
        ;;
    html)
        uv run manim-slides convert "${DECK[@]}" aion_talk.html --to html --one-file
        ;;
    *)
        sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
        exit 1
        ;;
esac
