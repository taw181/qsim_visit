# qsim_visit

commit and push frequently as you go.

Manim animations for a talk on single-photon atom clock interferometry
(AION: Sr clock transition, gradiometer baseline, large momentum transfer).

The project is two repos:

- `manim-atoms` (`github.com/taw181/manim-atoms`, private) — the package every animation comes from, installed as a dependency (`[tool.uv.sources]` in `pyproject.toml`; check it out beside this repo as `../manim-atoms` and point the source at it with `{ path = "../manim-atoms", editable = true }` to work on both at once). Anything reusable goes there, in its topic: `core`, `species`, `interferometry`, `trapping`, `aion` (gradiometer, GW, ULDM, AEDGE, km-scale, the DAI data), `slides` (the deck machinery). **Default home for new scenes, helpers and colours**; its own `CLAUDE.md` has its rules (one-way topic dependencies, per-topic `style.py`, no `manim_slides` outside `slides`, nothing about this talk).
- this repo — only what is specific to this talk:
  - `talk/aion_slides.py`: every slide (package scenes behind a mixin, static photo/figure slides, talk-only tweaks done by subclassing a package scene), plus the deck's own config: title, sections, `MEDIA`, `AION.bib`, the citation look, and `DeckSlide` / `Clicks` / `RunsOnIntoLoops` / `LoopingStages`, which are `manim_atoms.slides.deck`'s set to this deck.
  - `talk/deck.txt`: the deck's order.
  - `talk/deck.sh` and its no-bash twin `talk/deck.py`: render/present/html/player, thin wrappers round the package's `manim-atoms-deck`; keep the two in step.
  - `talk/build_player.py`: the web player's menu sections and names.
  - `talk/media/`: the talk's pictures and video.
  - `talk/extra_slides/`: slides taken out of the deck, e.g. LMT. They import `DeckSlide` from `aion_slides.py`, render and present by name, and have no footer number. One can still be played with the deck by an `extra_slides/x.py: XSlide` line in `deck.txt`, as HiFAIS is after the outro, and stays unnumbered.
  - Slide stops: a package scene calls a no-op hook (`beat()`; the sequence scenes' `stage_break()`) at each beat, and `Clicks` / `LoopingStages` turn it into `next_slide()`, so a slide is `class XSlide(Clicks, PackageScene)`. Where a subclass rewrites `construct`/`fly` without `super()`, the calls go in both. Every slide derives from `DeckSlide`, whose short settling hold (`SLIDE_SETTLE`) makes a slide stop on its finished frame (manim only draws an animation's last frame when the next one starts). `DeckSlide` also draws the footer (progress bar and slide number, from the slide's place in `deck.txt`) on top of everything; looping stops go through `RunsOnIntoLoops`, so a stage and its loop are one click.
  - Where the stops go, deck-wide: one stop once the apparatus and atoms are laid out; then each click is one pulse *and the legs it launches*, stopping as the atoms reach the next pulse (an extra stop only for an event mid-leg, e.g. the light-shift beam); the recombination click ends on the ports and readout; then one stop per annotation. The differential-interferometry, ULDM, GW and light-shift interferometer slides use the continuous variants (`GradiometerContinuous`, `DarkMatterPhaseContinuous`, `DarkMatterGradiometer` (continuous only), `GradiometerGWStretchContinuous`, `LightShiftSignalContinuous`): lab time never stops, so the whole pulse sequence to the ports is one click. A settling `wait` goes before a stop, never straight after one.
  - Citations: `AION.bib` (root, exported from Zotero) is the only source; `manim_atoms.bibliography` formats an entry under a `CiteFormat` (presets `FULL`, `SHORT`, `AUTHOR_YEAR`; vary with `dataclasses.replace`), `manim_atoms.core.citations` makes it a footer line. A slide sets `CITE = ("bibkey", ...)` (one line each) or `CITE = (("LIGO", "bibkey"), ...)` (run on as "LIGO: Aasi et al. (2015) · ..."), and `DeckSlide` draws it; `CITE_CORNER` moves it off content, `CITE_FORMAT` changes its look, or place `citation(...)` by hand. New references go into the Zotero AION collection (Better BibTeX re-exports `AION.bib` on change), never into `AION.bib` by hand.
  - Talk-side support: `plot_scripts/` save `manim_atoms.aion.plots` figures into `figures/`; `notes/` holds exported transcripts. The package's data and the scripts that regenerate it live in manim-atoms.

Working rules:

- A package scene on its own: `uv run manim -ql <path to manim_atoms>/<topic>/scenes/<file>.py <Scene>`, from this project's root so `manim.cfg` applies; `-qh` for the talk. Deck: `talk/deck.sh render [-j N] [-f FPS] [l|h] [Slide ...]` (`-j N`: N slides in parallel, one core each; logs in `media/deck_logs/`; `-f`: frame rate, default 30, `l` keeps 15; slides skip manim-slides' reversed copies), `talk/deck.sh present`, `talk/deck.sh html`, `talk/deck.sh player`; on Windows `uv run talk/deck.py` with the same arguments (the CLI passes `-q h`, not `-qh`: manim-slides reads the `h` as `--help`).
- After any change to a slide, always render the changed slides in low quality (`talk/deck.sh render l <Slide> ...`), check the frames, and end by giving the user both commands for those slides: to present them, `uv run manim-slides present <Slide> ...`, and to render them in high quality, `talk/deck.sh render h <Slide> ...`.
- A change to a package scene is made in manim-atoms, committed and pushed there, and this repo's pinned `rev` moved to it (`uv lock --upgrade-package manim-atoms`).
- Output: `media/videos/<script-stem>/<quality>/<Scene>.mp4` (gitignored).
- Imports are absolute (`from manim_atoms.interferometry.tools.clock import make_dial`), never relative: manim loads a scene file by path under a module name built from that path, so relative imports break. Star-import only `manim` and a style module (`aion_slides.py` takes `manim_atoms.aion.style`, which carries every palette); import names from topic modules explicitly, since they share names (`strain`, `GW_PERIOD`, ...).
- One-off scripts: `.venv/bin/python`.
- This is its own repo (`github.com/taw181/qsim_visit`), git root is the project root. Stage explicit paths — the working tree usually holds in-progress scripts of the user's, and `git add -A` will sweep them into your commit.
- Annotations belong where the physics happens: don't offset a recoil arrow off its atom to dodge an overlap — the overlap is fine.
- Measured data: `manim_atoms.aion.plots.dai_fringes` → AION DAI fringes and Lissajous ellipse (Zenodo 19592552); `manim_atoms.aion.plots.gw_sensitivity` → detector curves with merger tracks.
- Render-and-check loop, colour sampling, manim traps: the `manim-atom-interferometry` skill (its full version, `manim-atoms`, lives in the manim-atoms repo).
