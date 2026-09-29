"""A recorded video shown inside a scene, one frame at a time.

Manim has no video mobject, so the frames are decoded up front (with PyAV,
which manim already depends on) and swapped into one ImageMobject as the
scene runs. Which frame shows is up to the caller -- usually an updater
reading a ValueTracker -- so the video can be paused, held, or driven off
the same clock as the rest of the scene.
"""

import av
import numpy as np
from manim import *
from PIL import Image


def load_video_frames(path, every=1, crop=None):
    """Every ``every``-th frame of the video at ``path``, as RGBA arrays.

    ``crop`` is ``(top, bottom, left, right)`` in pixels, for trimming a
    border or a burnt-in caption too small to read once the video is shrunk
    into a corner.
    """
    with av.open(str(path)) as container:
        frames = [
            frame.to_ndarray(format="rgba")
            for i, frame in enumerate(container.decode(video=0))
            if i % every == 0
        ]
    if crop is not None:
        top, bottom, left, right = crop
        frames = [f[top:bottom, left:right].copy() for f in frames]
    return frames


class StreamedFrames:
    """The frames of the video at ``path``, decoded as they are asked for.

    A drop-in for ``load_video_frames``'s list where that list would be too
    big to hold: a 20 s video at 1080p60 is ten gigabytes of RGBA. Only the
    current frame is kept, scaled to ``width`` pixels (the height follows).
    Frames come cheapest in order, as a playing video asks for them; asking
    for an earlier one reopens the file and decodes forward to it.
    """

    def __init__(self, path, width=None):
        self.path = str(path)
        with av.open(self.path) as container:
            stream = container.streams.video[0]
            self.count = stream.frames
            self.rate = float(stream.average_rate)
            if width is None:
                width = stream.codec_context.width
            self.width = width
            self.height = round(width * stream.codec_context.height
                                / stream.codec_context.width / 2) * 2
        self._rewind()

    def _rewind(self):
        self._container = av.open(self.path)
        self._decoder = self._container.decode(video=0)
        self._index, self._frame, self._array = -1, None, None

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        if index < self._index:
            self._container.close()
            self._rewind()
        if index != self._index or self._array is None:
            while self._index < index:
                self._frame = next(self._decoder)
                self._index += 1
            # scaled by PIL: libswscale's own scaling (to_ndarray's width
            # and height) leaves a column of bright specks down the left edge
            image = self._frame.to_image()
            if image.size != (self.width, self.height):
                image = image.resize((self.width, self.height), Image.LANCZOS)
            self._array = np.asarray(image.convert("RGBA"))
        return self._array

    def __deepcopy__(self, memo):
        # an animation copies the mobject showing these; the file is shared
        return self


class VideoFrame(ImageMobject):
    """An image whose pixels can be swapped for another frame of a video.

    Don't animate its opacity: an animation interpolates the pixel array it
    started with and would paint over the frame swaps. Fade it with a
    background-coloured rectangle drawn on top instead.
    """

    def __init__(self, frames, **kwargs):
        super().__init__(frames[0], **kwargs)
        self.frames = frames
        self.index = 0

    def show(self, index):
        """Show frame ``index``, clamped to the frames there are."""
        index = int(np.clip(index, 0, len(self.frames) - 1))
        if index != self.index:
            self.pixel_array = self.frames[index].copy()
            self.orig_alpha_pixel_array = self.pixel_array[:, :, 3].copy()
            self.index = index
        return self
