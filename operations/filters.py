"""Built-in filter operations."""

from PIL import Image, ImageFilter, ImageEnhance

from operations.base import ImageOperation


class GrayscaleFilter(ImageOperation):
    name = "Grayscale"

    def apply(self, image: Image.Image) -> Image.Image:
        return image.convert("L").convert("RGB")


class BlurFilter(ImageOperation):
    def __init__(self, radius: float = 2.0) -> None:
        self._radius = radius

    name = "Blur"

    def apply(self, image: Image.Image) -> Image.Image:
        return image.filter(ImageFilter.GaussianBlur(radius=self._radius))


class SharpenFilter(ImageOperation):
    name = "Sharpen"

    def apply(self, image: Image.Image) -> Image.Image:
        return image.filter(ImageFilter.SHARPEN)


class SepiaFilter(ImageOperation):
    name = "Sepia"

    def apply(self, image: Image.Image) -> Image.Image:
        grey = image.convert("L")
        r = grey.point(lambda p: min(255, int(p * 1.08)))
        g = grey.point(lambda p: min(255, int(p * 0.85)))
        b = grey.point(lambda p: min(255, int(p * 0.66)))
        return Image.merge("RGB", (r, g, b))


class BrightnessFilter(ImageOperation):
    def __init__(self, factor: float = 1.3) -> None:
        self._factor = factor

    name = "Brightness"

    def apply(self, image: Image.Image) -> Image.Image:
        return ImageEnhance.Brightness(image).enhance(self._factor)


class ContrastFilter(ImageOperation):
    def __init__(self, factor: float = 1.3) -> None:
        self._factor = factor

    name = "Contrast"

    def apply(self, image: Image.Image) -> Image.Image:
        return ImageEnhance.Contrast(image).enhance(self._factor)


# Registry: maps display name → operation factory (no-arg callable)
FILTER_REGISTRY: dict[str, type[ImageOperation]] = {
    "Grayscale": GrayscaleFilter,
    "Blur": BlurFilter,
    "Sharpen": SharpenFilter,
    "Sepia": SepiaFilter,
    "Brightness +": BrightnessFilter,
    "Contrast +": ContrastFilter,
}
