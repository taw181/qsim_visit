"""The Freiburg talk as one manim-slides deck, in the order of the talk.

Intro, atom interferometry, gravitational waves, dark matter, the prototype,
future plans, outro. The animated slides are manim_atoms scenes, picked up unmodified
through multiple inheritance; the static ones (title, contents, photographs,
figures) are laid out here, with the pictures in talk/media/.

A scene marks where the presenter should stop by calling a hook, and the
wrappers -- manim_atoms.slides.deck's, configured for this deck below -- turn
the hook into a slide break:

- beat() is a no-op in the package; Clicks makes it a plain stop. Nothing in
  those scenes moves while they are paused, so there is nothing to loop.
- stage_break() is the sequence scenes' timed hold; LoopingStages loops two
  seconds of it instead, so the cloud keeps moving while a stage is talked
  through.
- hold() is DarkMatterField's one period of the field; the slide loops it.
  (DarkMatterScale's too, on its slide in extra_slides/uldm_scale_slides.py.)

A looping stop is still one click: RunsOnIntoLoops plays each stretch straight
on into its loop, and the click moves on from the loop.

The deck order lives in talk/deck.txt; talk/deck.sh renders, presents and
converts it (through manim_atoms' manim-atoms-deck):

    talk/deck.sh render h     # -q h; `l` for a quick look
    talk/deck.sh present
    talk/deck.sh html         # aion_talk.html, standalone
"""

from dataclasses import replace
from pathlib import Path

from manim import *

from manim_atoms.bibliography import (
    AUTHOR_YEAR,
    FULL,
    SHORT,
    format_reference,
    load_bibliography,
)
from manim_atoms.aion.style import *
from manim_atoms.aion.scenes.aedge import AEDGESensitivity
from manim_atoms.interferometry.scenes.clock import ClockPhaseTerms
from manim_atoms.interferometry.scenes.gradiometer import GradiometerContinuous
from manim_atoms.trapping.scenes.cooling import CoolingSequence
from manim_atoms.aion.scenes.dai_data import LaserNoiseLissajous
from manim_atoms.trapping.scenes.dipole import DipoleTrapLoading
from manim_atoms.aion.scenes.gradiometer_gw import GradiometerGWStretchContinuous
from manim_atoms.aion.scenes.gravitational_waves import (
    BlackHoleMerger,
    MergerOnSensitivityPlot,
)
from manim_atoms.aion.scenes.ligo import LIGOMichelson
from manim_atoms.aion.scenes.gw_landscape import SensitivityBuildUp
from manim_atoms.aion.scenes.km_challenges import KmScaleChallenges
from manim_atoms.aion.scenes.light_shift import LightShiftSignalContinuous
from manim_atoms.aion.scenes.signal_injection import SignalInjection
from manim_atoms.trapping.scenes.sequence import SEQ_SIMPLE_REFERENCES, ExperimentSequenceSimple
from manim_atoms.interferometry.scenes.single_photon import SinglePhotonMachZehnder
from manim_atoms.trapping.scenes.slicing import VelocitySlicing
from manim_atoms.aion.scenes.uldm import (
    DarkMatterField,
    DarkMatterGradiometer,
    DarkMatterPhaseContinuous,
)
from manim_atoms.aion.scenes.uldm_scale import DarkMatterScalePlot
from manim_atoms.core.citations import labelled_citation
from manim_atoms.core.layout import image_point, load_image, numbered_list, slide_title
from manim_atoms.core.primitives import make_cloud
from manim_atoms.core.video import VideoFrame, load_video_frames
from manim_atoms.slides import deck

MEDIA = Path(__file__).parent / "media"
# The measured-data plots plot_scripts/ draw from the package data.
FIGURES = Path(__file__).parent.parent / "figures"
# The talk's references, exported from the Zotero collection; a slide cites
# them by key through DeckSlide.CITE.
BIB = load_bibliography(Path(__file__).parent.parent / "AION.bib")
# How a slide's footer citation reads. replace() it for another look: keep=
# names an author through the et al., collaboration= replaces the list.
CITE_FORMAT = replace(SHORT, highlight=("Walker, T",))
# ...and a slide citing many papers, as (label, key) pairs, run on together
CITE_LABELLED_FORMAT = replace(AUTHOR_YEAR, highlight=("Walker, T",))

TITLE = (r"A prototype differential atom interferometer", r"for fundamental physics")
AUTHOR = r"Thomas Walker"
VENUE = r"@ Albert-Ludwigs Universit\"at Freiburg, 2026"
SECTIONS = (
    r"Atom interferometry",
    r"Motivation",
    r"Our prototype device",
    r"Future plans",
)
# The title slide's background: the video's own frame rate, and how much of
# it the veil over it takes back so the title reads.
TITLE_VIDEO_FPS = 15
TITLE_VEIL_OPACITY = 0.55
# How long each slide holds its last frame before it stops (see
# manim_atoms.slides.deck.DeckSlide.SETTLE).
SLIDE_SETTLE = 0.1
# The deck's order: the footer numbers each slide by its place in it.
DECK = deck.load_deck(Path(__file__).parent / "deck.txt")


def cite(*keys):
    """The deck's references under these keys, failing on one not in AION.bib."""
    return deck.cite(BIB, *keys)


# --- how a scene's hooks become slide breaks -------------------------------
# The machinery is manim_atoms.slides.deck's; this deck only says which deck
# file it numbers its slides from, where its references are, and how they read.
class DeckSlide(deck.DeckSlide):
    """Every slide in the deck: manim_atoms' DeckSlide, numbered from
    talk/deck.txt, citing AION.bib."""

    DECK = DECK
    BIB = BIB
    CITE_FORMAT = CITE_FORMAT
    CITE_LABELLED_FORMAT = CITE_LABELLED_FORMAT
    SETTLE = SLIDE_SETTLE


class Clicks(deck.Clicks, DeckSlide):
    """beat() stops and waits for the presenter."""


class RunsOnIntoLoops(deck.RunsOnIntoLoops, DeckSlide):
    """Each stretch plays straight on into its loop: a stage is one click."""


class LoopingStages(deck.LoopingStages, RunsOnIntoLoops):
    """stage_break() loops two seconds of the running stage until the click."""


# --- intro -------------------------------------------------------------------
class TitleSlide(DeckSlide):
    """The title over the blue MOT, with the video running for as long as the
    slide is up: driven forwards and then backwards, so the loop has no seam."""

    def construct(self):
        frames = load_video_frames(MEDIA / "blue_mot.mp4")
        video = VideoFrame(frames)
        video.width = config.frame_width
        cycle = 2 * (len(frames) - 1)  # there and back, in frames
        clock = ValueTracker(0.0)

        def ping_pong(m):
            f = clock.get_value() % cycle
            m.show(round(f if f <= cycle / 2 else cycle - f))

        video.add_updater(ping_pong)
        # The video cannot be faded (see VideoFrame), so a veil drawn over it
        # lifts instead, and stops part way to keep the text readable.
        veil = FullScreenRectangle(
            stroke_width=0, fill_color=PLOT_BACKGROUND, fill_opacity=1.0
        )

        aion = load_image(MEDIA / "aion_logo_on_dark.png", height=1.0)
        imperial = load_image(MEDIA / "imperial_logo_on_dark.png", height=0.42)
        aion.to_corner(UL, buff=0.4)
        imperial.to_corner(UR, buff=0.4).match_y(aion)
        title = VGroup(*[Tex(line, font_size=FONT_DECK_TITLE) for line in TITLE])
        title.arrange(DOWN, buff=0.25)
        byline = VGroup(
            Tex(AUTHOR, font_size=FONT_DECK_BYLINE),
            Tex(VENUE, font_size=FONT_DECK_BYLINE, color=lighten(GUIDE_COLOR)),
        ).arrange(DOWN, buff=0.18)
        # In the bottom half, clear of the MOT near the middle of the frame.
        VGroup(title, byline).arrange(DOWN, buff=0.5).to_edge(DOWN, buff=0.6)

        self.add(video, veil)
        self.next_slide(auto_next=True)  # straight on into the loop
        fade_in = 1.5
        self.play(
            veil.animate.set_fill(opacity=TITLE_VEIL_OPACITY),
            FadeIn(aion),
            FadeIn(imperial),
            FadeIn(title),
            FadeIn(byline),
            clock.animate.increment_value(fade_in * TITLE_VIDEO_FPS),
            rate_func=linear,
            run_time=fade_in,
        )
        self.next_slide(loop=True)
        self.play(
            clock.animate.increment_value(cycle),
            rate_func=linear,
            run_time=cycle / TITLE_VIDEO_FPS,
        )


class ContentsSlide(DeckSlide):
    def construct(self):
        contents = numbered_list(SECTIONS).move_to(DOWN * 0.2)
        self.play(FadeIn(slide_title(r"Outline")), FadeIn(contents), run_time=0.8)


class SectionSlide(DeckSlide):
    """A section's title, numbered as it is in the outline."""

    SECTION = None  # one of SECTIONS

    def construct(self):
        number = SECTIONS.index(self.SECTION) + 1
        title = VGroup(
            Tex(f"{number}.", font_size=FONT_DECK_TITLE, color=lighten(GUIDE_COLOR)),
            Tex(self.SECTION, font_size=FONT_DECK_TITLE),
        ).arrange(RIGHT, buff=0.35)
        self.play(FadeIn(title), run_time=0.8)


# --- atom interferometry ----------------------------------------------------
class AtomInterferometrySlide(SectionSlide):
    SECTION = r"Atom interferometry"


class SinglePhotonMachZehnderSlide(Clicks, SinglePhotonMachZehnder):
    pass


class ClockPhaseTermsSlide(Clicks, ClockPhaseTerms):
    pass


class GradiometerSlide(Clicks, GradiometerContinuous):
    pass


# --- motivation: gravitational waves, then dark matter ---------------------
class MotivationSlide(SectionSlide):
    SECTION = r"Motivation"


# The sensitivity curves are digitised from an internal AION figure, whose
# own sources aren't known, so each detector cites the paper that set it out;
# the merger tracks cite their waveform model and the cosmology that sets
# their distances.
LIGO_PAPER = ("LIGO", "LIGOScientific:2014pky")
MERGER_PAPERS = (("mergers", "Ajith:2007kx"), ("Planck", "Planck:2018vyg"))

# The recorded data on the left panel is GW150914 itself: its ~1000-author
# byline stands in for the collaboration, the way papers like it are usually
# cited, rather than truncating to one name and "et al.".
GW150914_KEY = (
    "ligoscientificcollaborationandvirgocollaborationObservationGravitationalWaves2016"
)
GW150914_FORMAT = replace(CITE_LABELLED_FORMAT, collaboration="LIGO Collaboration")


class BlackHoleMergerSlide(DeckSlide, BlackHoleMerger):
    """No stops: the merger plays straight through from the moment the slide
    comes up, and holds on the settled sheet as the slide's own end."""


class LIGOMichelsonSlide(Clicks, LIGOMichelson):
    """The Michelson on its dark port, a stop, then a wave passes and lights
    it up."""

    CITE = (LIGO_PAPER,)


class MergerOnSensitivityPlotSlide(Clicks, MergerOnSensitivityPlot):
    """The merger beside the sensitivity plot: a stop once laid out and once
    settled.

    The left panel becomes real LIGO data at the end, so its citation joins
    the detector paper under the same "LIGO" label."""

    TITLE = r"LIGO's first GW detection"
    CITE = (LIGO_PAPER, *MERGER_PAPERS)
    CITE_CORNER = DR  # under the plot, clear of the LIGO figure's time axis

    def citation(self):
        ligo = [
            *cite("LIGOScientific:2014pky"),
            format_reference(BIB[GW150914_KEY], GW150914_FORMAT),
        ]
        items = [
            ("LIGO", ligo),
            *[(label, cite(*keys)) for label, *keys in MERGER_PAPERS],
        ]
        return labelled_citation(items, fmt=CITE_LABELLED_FORMAT)


class SensitivityLandscapeSlide(Clicks, SensitivityBuildUp):
    """The landscape without AEDGE: AION's three stages fill the gap."""

    GAP_FILLERS = ("AION-10", "AION-100", "AION-km")
    TITLE = r"Gravitational wave sensitivity landscape"
    # brought down under the title, and up off the citation lines
    PLOT_ORIGIN = np.array([-4.9, -2.45, 0.0])
    PLOT_HEIGHT = 5.3
    CITE = (
        LIGO_PAPER,
        ("LISA", "LISA:2017pwj"),
        ("ET", "Punturo:2010zz"),
        ("AION-10/100/km", "badurinaAIONAtomInterferometer2020"),
        *MERGER_PAPERS,
    )


class GradiometerGWStretchSlide(Clicks, GradiometerGWStretchContinuous):
    """Continuous: lab time never stops between the first pulse and the ports,
    so the far cloud visibly splits L/c after the near one. One click runs the
    whole sequence; the stops are the set-up before it and the readout after."""


class DarkMatterScaleSlide(Clicks, DarkMatterScalePlot):
    """The plot up, then a click per mass, each labelled with how long its
    wave is, and one for the verdict. The fly-out across the solar system it
    replaces is DarkMatterScaleFlyoutSlide, in extra_slides/."""

    CITE = ("badurinaAIONAtomInterferometer2020",)  # the curves


class DarkMatterFieldSlide(RunsOnIntoLoops, DarkMatterField):
    def hold(self):
        self.loop(super().hold)


class DarkMatterPhaseSlide(Clicks, DarkMatterPhaseContinuous):
    """Continuous: the field keeps oscillating while the pulses fire, so one
    click runs the interferometer from the first pulse to the ports."""


class DarkMatterGradiometerSlide(Clicks, DarkMatterGradiometer):
    """The same field through the gradiometer, continuous like the rest: one
    click runs both interferometers from the first pulse to the ports, the far
    cloud L/c behind the near one."""


# --- our prototype device -------------------------------------------------
class PrototypeDeviceSlide(SectionSlide):
    SECTION = r"Our prototype device"


# plot_scripts/aion_baselines.py draws the sketches on a 3840 px-wide frame:
# placed at that scale, its line weights match the rest of the deck
BASELINE_PX_PER_UNIT = 3840 / config.frame_width


class AIONCollabSlide(DeckSlide):
    """Who AION are and where, and the kilometre baseline they are building
    towards: four interferometers along one shaft."""

    def construct(self):
        title = slide_title(r"The AION collaboration")
        logo = load_image(MEDIA / "aion_logo_on_dark.png", height=1.0)
        logo.to_corner(UR, buff=0.4)
        uk_map = load_image(MEDIA / "aion_map.jpeg", height=6.0).move_to(
            LEFT * 2.0 + DOWN * 0.45
        )
        baseline = load_image(FIGURES / "aion_km_baseline.png")
        baseline.height = baseline.pixel_array.shape[0] / BASELINE_PX_PER_UNIT
        baseline.move_to(RIGHT * 3.6 + DOWN * 0.45)
        self.play(
            FadeIn(title), FadeIn(logo), FadeIn(uk_map), FadeIn(baseline),
            run_time=0.8,
        )


# The dark window between the coils in chamber_cropped.png (2475 x 1548 px),
# upper left and lower right: where the two clouds sit.
CHAMBER_WINDOW_PX = ((1090, 705), (1375, 900))
CHAMBER_GAP = 2.2  # between the cartoon clouds' centres, on screen


class ChamberSlide(DeckSlide):
    """Our chamber, with its centre called out: two atom clouds about 2 mm
    apart, then how that compares with AION's kilometre."""

    def construct(self):
        title = slide_title(r"Our prototype")
        photo = load_image(MEDIA / "chamber_cropped.png", height=5.2)
        photo.to_edge(LEFT, buff=0.4).set_y(-0.45)
        ul, dr = [image_point(photo, *p) for p in CHAMBER_WINDOW_PX]
        box = Rectangle(
            width=dr[0] - ul[0],
            height=ul[1] - dr[1],
            stroke_color=CALLOUT_COLOR,
            stroke_width=CALLOUT_STROKE_WIDTH,
        ).move_to((ul + dr) / 2)

        panel = RoundedRectangle(
            corner_radius=CALLOUT_CORNER_RADIUS,
            width=config.frame_x_radius - 0.4 - photo.get_right()[0] - 0.6,
            height=photo.height,
            stroke_color=CALLOUT_COLOR,
            stroke_width=CALLOUT_STROKE_WIDTH,
            fill_color=PLOT_BACKGROUND,
            fill_opacity=1,
        )
        panel.next_to(photo, RIGHT, buff=0.6).match_y(photo)
        joins = VGroup(
            Line(box.get_corner(UR), panel.get_corner(UL)),
            Line(box.get_corner(DR), panel.get_corner(DL)),
        ).set_stroke(CALLOUT_COLOR, CALLOUT_STROKE_WIDTH)

        lower = make_cloud(DOWN * CHAMBER_GAP / 2, LOWER_CLOUD_COLOR, seed=1)
        upper = make_cloud(UP * CHAMBER_GAP / 2, UPPER_CLOUD_COLOR, seed=2)
        gap = DoubleArrow(
            DOWN * CHAMBER_GAP / 2,
            UP * CHAMBER_GAP / 2,
            buff=0,
            stroke_width=4,
            color=lighten(GUIDE_COLOR),
            max_tip_length_to_length_ratio=0.12,
        ).shift(RIGHT * (CARTOON_CLOUD_RADIUS + 0.25))
        label = MathTex(
            r"\sim\!2\,\mathrm{mm}", r"\ll 1\,\mathrm{km}", font_size=FONT_ANNOTATION
        )
        label.next_to(gap, RIGHT, buff=0.15)
        # centred as it ends up, with the km in, so nothing moves when it arrives
        VGroup(lower, upper, gap, label).move_to(panel)

        self.play(
            FadeIn(title),
            FadeIn(photo),
            FadeIn(box),
            FadeIn(joins),
            FadeIn(panel),
            FadeIn(lower),
            FadeIn(upper),
            FadeIn(gap),
            FadeIn(label[0]),
            run_time=0.8,
        )
        self.next_slide()
        self.play(FadeIn(label[1], shift=LEFT * 0.2), run_time=0.6)


class AIONChambersSlide(DeckSlide):
    """The same chamber built at each AION site in 2022: the photos carry
    their own captions."""

    CITE = ("strayCentralizedDesignProduction2024",)

    def construct(self):
        title = slide_title(r"AION chambers across the UK")
        # ends above the citation line rather than under it
        figure = load_image(MEDIA / "aion_chambers.png", height=6.3)
        figure.next_to(title, DOWN, buff=0.25).set_x(0)
        self.play(FadeIn(title), FadeIn(figure), run_time=0.8)


class ExperimentSequenceSlide(DeckSlide, ExperimentSequenceSimple):
    """No stops: the shot plays through to the loaded lower trap and holds
    there. Its reference list is from AION.bib, in full, and as in the
    package cut to the papers its stages cite."""

    REFERENCES = [
        format_reference(ref, FULL)
        for ref in cite(
            "strayCentralizedDesignProduction2024",
            "pasatembouProgressUltracoldSr2024",
            "baynhamPrototypeDifferentialAtom2026",
        )
    ][:SEQ_SIMPLE_REFERENCES]


class CoolingSequenceSlide(LoopingStages, CoolingSequence):
    CITE = ("pasatembouProgressUltracoldSr2024",)


class DipoleTrapLoadingSlide(LoopingStages, DipoleTrapLoading):
    pass


class VelocitySlicingSlide(LoopingStages, VelocitySlicing):
    pass


# The paper the prototype's results are from.
DAI_PAPER = "baynhamPrototypeDifferentialAtom2026"


class LightShiftSignalSlide(Clicks, LightShiftSignalContinuous):
    """Continuous: lab time never stops from the first pulse to the imaging,
    so the beam is a window the atoms fly through. The readout ends on the
    camera image of the two clouds, S left and P right, in place of the
    dials."""

    CITE = (DAI_PAPER,)
    CITE_CORNER = UR  # bottom left is the laser's label

    # the image's two columns, as fractions of its width from the left
    IMAGE_COLUMNS = {"S": (0.27, ATOM_COLOR), "P": (0.78, KICKED_COLOR)}

    def readout_image(self):
        image = load_image(MEDIA / "atom_phase_image.png", height=5.4)
        image.to_edge(RIGHT, buff=0.25).set_y(-0.25)
        left, width = image.get_left()[0], image.width
        labels = VGroup(
            *[
                Tex(name, font_size=FONT_STATE, color=lighten(color)).move_to(
                    [left + f * width, image.get_top()[1] + 0.3, 0]
                )
                for name, (f, color) in self.IMAGE_COLUMNS.items()
            ]
        )
        return Group(image, labels)


class SignalInjectionSlide(LoopingStages, SignalInjection):
    CITE = (DAI_PAPER,)


class LaserNoiseLissajousSlide(Clicks, LaserNoiseLissajous):
    """The quiet run full size, then shrunk to the top panel with the noisy
    run below it, both onto the one Lissajous plot."""

    CITE = (DAI_PAPER,)


class AllanDeviationSlide(DeckSlide):
    """The differential phase's Allan deviation, from
    plot_scripts/interferometer_data.py: the standard quantum limit with the
    quiet and noisy runs on it, all at once."""

    CITE = (DAI_PAPER,)

    def construct(self):
        title = slide_title(r"Allan deviation")
        adev = load_image(FIGURES / "adev.png", height=6.6)
        adev.next_to(title, DOWN, buff=0.2).set_x(0)
        self.play(FadeIn(title), FadeIn(adev), run_time=0.8)


class ExtractedSignalSlide(DeckSlide):
    """Fig. 5a redrawn: each imprinted frequency found where it was put."""

    CITE = (DAI_PAPER,)

    def construct(self):
        title = slide_title(r"Extracted signals")
        figure = load_image(FIGURES / "signals.png", width=13.4)
        figure.next_to(title, DOWN, buff=0.35).set_x(0)
        self.play(FadeIn(title), FadeIn(figure), run_time=0.8)


# --- future plans ---------------------------------------------------------
class FuturePlansSlide(SectionSlide):
    SECTION = r"Future plans"


class KmChallengesSlide(Clicks, KmScaleChallenges):
    """The headings, then one challenge per click: the prototype's figures
    beside AION-km's (its Table 1) and what they ask for."""

    CITE = (DAI_PAPER, "badurinaAIONAtomInterferometer2020")


class Aion10BeecroftSlide(DeckSlide):
    """The 10 m baseline, the building cut away round it, then the stairwell
    it runs down, one per click left to right -- laid out as the row they end
    up in, so nothing moves.
    The building is a tall, narrow cutaway, so it takes nearly the full height
    of the slide to be legible; it sits right of the title, so it can rise
    level with it."""

    CITE = ("bongsAION10TechnicalDesign2025",)

    def construct(self):
        title = slide_title(r"AION-10 at Oxford")
        # AION-km's sketch with two sources along 10 m, at the deck's line weights
        baseline = load_image(FIGURES / "aion_10_baseline.png")
        baseline.height = baseline.pixel_array.shape[0] / BASELINE_PX_PER_UNIT
        stairwell = load_image(MEDIA / "stairwell.jpg", height=4.9)
        building = load_image(MEDIA / "beecroft.jpeg", height=config.frame_height - 0.4)
        Group(baseline, building, stairwell).arrange(RIGHT, buff=0.7).set_x(0.2)
        baseline.set_y(-0.45)
        stairwell.set_y(-0.45)
        building.set_y(0)

        # left to right, one per click
        self.play(FadeIn(title), FadeIn(baseline), run_time=0.8)
        self.next_slide()
        self.play(FadeIn(building, shift=LEFT * 0.3), run_time=0.8)
        self.next_slide()
        self.play(FadeIn(stairwell, shift=LEFT * 0.3), run_time=0.8)


# The PX46 shaft in aice.png (1199 x 672 px): from under the surface building
# down to its rounded foot, with the arrow just clear of its right-hand side.
AICE_SHAFT_PX = ((940, 207), (940, 525))
# The bottom edge of the figure's title box, which the points box goes under.
AICE_TITLE_BOTTOM_PX = 197
# Small enough that the box clears the yellow PX46 shaft and its label below.
AICE_POINTS_FONT = 26


class AICECernSlide(DeckSlide):
    """The AICE figure, which carries its own title, with the shaft's depth
    marked on it and what it is for in a box under the title."""

    CITE = ("arduiniTechnicalProposalAtom2026",)

    def citation(self):
        # the figure runs edge to edge, so the line sits on the photo: outlined
        # in the background colour, as the slide number is
        return super().citation().set_stroke(PLOT_BACKGROUND, width=4, background=True)

    def construct(self):
        figure = load_image(MEDIA / "aice.png", width=config.frame_width)

        def at(px, py):
            """A pixel of aice.png, on screen."""
            return figure.get_corner(UL) + [
                px / 1199 * figure.width,
                -py / 672 * figure.height,
                0,
            ]

        depth = DoubleArrow(
            *[at(*p) for p in AICE_SHAFT_PX],
            buff=0,
            stroke_width=PHOTO_LABEL_STROKE_WIDTH,
            color=PHOTO_LABEL_COLOR,
            tip_length=0.3,
            max_tip_length_to_length_ratio=0.1,
            max_stroke_width_to_length_ratio=10,
        )
        label = Tex(
            r"\textbf{150\,m}", font_size=FONT_PHOTO_LABEL, color=PHOTO_LABEL_COLOR
        )
        label.next_to(depth, RIGHT, buff=0.15)
        depth.set_stroke(**PHOTO_LABEL_OUTLINE, background=True, family=False)
        label.set_stroke(**PHOTO_LABEL_OUTLINE, background=True)

        # what it is for, in a box like the figure's own title box, under it
        points = VGroup(*(
            Tex(rf"\textsf{{\textbf{{{line}}}}}", font_size=AICE_POINTS_FONT,
                color=WHITE)
            for line in (
                r"\textbullet\ Sr \& Yb atoms",
                r"\textbullet\ ULDM",
                r"\textbullet\ $\boldsymbol{\alpha}$ measurement",
                r"\textbullet\ Test of equivalence principle",
            )
        )).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        underway = Tex(r"\textsf{\textbf{Construction underway!}}",
                       font_size=AICE_POINTS_FONT, color=PHOTO_LABEL_COLOR)
        underway.next_to(points, DOWN, buff=0.22, aligned_edge=LEFT)
        text = VGroup(points, underway)
        box = SurroundingRectangle(
            text, buff=0.25, stroke_color=BLACK, stroke_width=1.5,
            fill_color=BLACK, fill_opacity=0.55,
        )
        panel = VGroup(box, text)
        panel.next_to(at(0, AICE_TITLE_BOTTOM_PX), DR, buff=0).shift(
            RIGHT * 0.25 + DOWN * 0.12
        )
        self.play(FadeIn(figure), FadeIn(depth), FadeIn(label), FadeIn(panel),
                  run_time=0.8)


class AEDGESlide(Clicks, AEDGESensitivity):
    """The two sensitivity plots as the talk has shown them, then a click
    puts AEDGE on both."""

    CITE = (
        LIGO_PAPER,
        ("LISA", "LISA:2017pwj"),
        ("ET", "Punturo:2010zz"),
        ("AION", "badurinaAIONAtomInterferometer2020"),
        ("AEDGE", "AEDGE:2019nxb"),
    )


# --- outro -------------------------------------------------------------------
class OutroSlide(DeckSlide):
    """Thank you: the Sr lab team down the left; Oliver and the AION logo
    over the AION collaboration down the right."""

    def construct(self):
        def labelled(image, text):
            label = Tex(text, font_size=FONT_LEGEND, color=lighten(GUIDE_COLOR))
            return Group(image, label.next_to(image, DOWN, buff=0.15))

        title = slide_title(r"Thank you for listening!")
        sr_group = labelled(
            load_image(MEDIA / "sr_lab_group.jpg", height=5.2), r"Sr lab team"
        )
        oliver = labelled(
            load_image(MEDIA / "oliver.png", height=2.3), r"Oliver Buchm\"uller, PI"
        )
        logo = load_image(MEDIA / "aion_logo_on_white.png", height=1.3)
        aion_group = labelled(
            load_image(MEDIA / "aion_group.png", width=6.0), r"AION collaboration"
        )
        top_right = Group(oliver, logo).arrange(RIGHT, buff=0.6)
        logo.match_y(oliver[0])
        right = Group(top_right, aion_group).arrange(DOWN, buff=0.3)
        Group(sr_group, right).arrange(RIGHT, buff=0.5).next_to(
            title, DOWN, buff=0.3
        ).set_x(0)
        self.play(FadeIn(title), FadeIn(sr_group), FadeIn(right), run_time=0.8)
