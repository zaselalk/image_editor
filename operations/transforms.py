"""Geometric transformation operations."""

from PIL import Image

from operations.base import ImageOperation


class RotateCW(ImageOperation):
    name = "Rotate 90° CW"

    def apply(self, image: Image.Image) -> Image.Image:
        return image.rotate(-90, expand=True)


class RotateCCW(ImageOperation):
    name = "Rotate 90° CCW"

    def apply(self, image: Image.Image) -> Image.Image:
        return image.rotate(90, expand=True)


class FlipHorizontal(ImageOperation):
    name = "Flip Horizontal"

    def apply(self, image: Image.Image) -> Image.Image:
        return image.transpose(Image.FLIP_LEFT_RIGHT)


class FlipVertical(ImageOperation):
    name = "Flip Vertical"

    def apply(self, image: Image.Image) -> Image.Image:
        return image.transpose(Image.FLIP_TOP_BOTTOM)


class CropOperation(ImageOperation):
    """Crop to a box (left, upper, right, lower) in pixel coordinates."""

    name = "Crop"

    def __init__(self, box: tuple[int, int, int, int]) -> None:
        self._box = box

    def apply(self, image: Image.Image) -> Image.Image:
        return image.crop(self._box)
