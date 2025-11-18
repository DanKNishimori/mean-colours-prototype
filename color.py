from random import uniform
from typing import Union, Callable

Bytes = list["Byte"]
Colors = list["Color"]
Number = Union[int, float]

BYTE_MIN = 0
BYTE_MAX = 255


def clip(base: Number, min_v: Number, max_v: Number) -> Number:
    if base < min_v:
        return min_v
    elif base > max_v:
        return max_v
    return base


def fill_sequence(n0: int, nf: int, l: int) -> list[int]:
    form: Callable[[int], float] = lambda idx: n0 + (idx - 1) * (nf - n0) / (l - 1)
    return [int(form(i)) for i in range(1, l + 1)]


def random_deviation(
    target: Number,
    dev_level: float,
    min_range: tuple[int, int],
    max_range: tuple[int, int],
) -> float:
    min_v = clip(target * abs(dev_level - 1), min_range[0], min_range[1])
    max_v = clip(target * abs(dev_level + 1), max_range[0], max_range[1])
    return uniform(min_v, max_v)


class Byte:
    def __init__(self, value: int):
        self.value = int(clip(value, BYTE_MIN, BYTE_MAX))

    @staticmethod
    def from_str(value: str) -> "Byte":
        return Byte(int(value, 16))

    def as_int(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"{hex(self.value)[2:]:0>2}"

    def __add__(self, target: "Byte") -> "Byte":
        return Byte(self.value + target.value)

    def __sub__(self, target: "Byte") -> "Byte":
        return Byte(self.value - target.value)


class Color:
    def __init__(self, color: str | tuple[int, int, int]):
        if type(color) is tuple[int, int, int]:
            self.red = Byte(color[0])
            self.green = Byte(color[1])
            self.blue = Byte(color[2])
        else:
            color_code = str(color).replace("#", "")
            self.red = Byte.from_str(color_code[0:2])
            self.green = Byte.from_str(color_code[2:4])
            self.blue = Byte.from_str(color_code[4:6])

    @staticmethod
    def from_bytes(r: "Byte", g: "Byte", b: "Byte") -> "Color":
        return Color((r.as_int(), g.as_int(), b.as_int()))

    @staticmethod
    def zip_rgb(*args: "Color") -> tuple[Bytes, Bytes, Bytes]:
        r: Bytes = []
        g: Bytes = []
        b: Bytes = []
        for i in args:
            r.append(i.red)
            g.append(i.green)
            b.append(i.blue)
        return (r, g, b)

    @staticmethod
    def mean(colors: Colors) -> "Color":
        red, green, blue = 0, 0, 0
        length = len(colors)
        for c in colors:
            red += c.red.as_int()
            green += c.green.as_int()
            blue += c.blue.as_int()
        return Color((int(red / length), int(green / length), int(blue / length)))

    @staticmethod
    def make_sequence(first_color: "Color", last_color: "Color", length: int) -> Colors:
        (reds, greens, blues) = Color.zip_rgb(first_color, last_color)
        reds = fill_sequence(reds[0].as_int(), reds[1].as_int(), length)
        greens = fill_sequence(greens[0].as_int(), greens[1].as_int(), length)
        blues = fill_sequence(blues[0].as_int(), blues[1].as_int(), length)
        return [Color(rgb) for rgb in zip(reds, greens, blues)]

    def invert(self) -> "Color":
        return Color.from_bytes(
            Byte(255) - self.red,
            Byte(255) - self.green,
            Byte(255) - self.blue,
        )

    def derive_randomly(self, dev_level: float) -> "Color":
        max_range, min_range = (5, 255), (0, 255)
        [red, green, blue] = [
            random_deviation(self.red.as_int(), dev_level, min_range, max_range),
            random_deviation(self.green.as_int(), dev_level, min_range, max_range),
            random_deviation(self.blue.as_int(), dev_level, min_range, max_range),
        ]
        return Color((int(red), int(green), int(blue)))

    def __repr__(self) -> str:
        return f"Color<R={self.red};G={self.green};B={self.blue}>"

    def __str__(self) -> str:
        return f"#{self.red}{self.green}{self.blue}"

    def __add__(self, value: "Color") -> "Color":
        return Color.from_bytes(
            self.red + value.red, self.green + value.green, self.blue + value.blue
        )

    def __sub__(self, value: "Color") -> "Color":
        return Color.from_bytes(
            self.red - value.red, self.green - value.green, self.blue - value.blue
        )
