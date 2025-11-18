from random import uniform
from typing import Union

Bytes = list["Byte"]


def clip(base: int | float, min_v: int | float, max_v: int | float) -> int | float:
    if base < min_v:
        return min_v
    elif base > max_v:
        return max_v
    return base


def fill_sequence(n0: int | float, nf: int | float, l: int) -> list[int]:
    form = lambda idx: n0 + (idx - 1) * (nf - n0) / (l - 1)
    return [int(form(i)) for i in range(1, l + 1)]


def random_deviation(
    target: int | float, dev_level: float, min_range=(0, 2**8), max_range=(0, 2**8)
) -> float:
    min_v = clip(target * abs(dev_level - 1), min_range[0], min_range[1])
    max_v = clip(target * abs(dev_level + 1), max_range[0], max_range[1])
    return uniform(min_v, max_v)


class Byte:
    def __init__(self, value: int):
        self.value = int(clip(value, 0, 255))

    def from_str(value: str) -> "Byte":
        return Byte(int(value, 16))

    def as_int(self) -> int:
        return self.value

    def __repr__(self) -> str:
        num = hex(self.value).replace("0x", "")
        return "0" + num if len(num) < 2 else num

    def __add__(self, target: Union["Byte", int]) -> "Byte":
        value: int = target.value if type(target) is Byte else target
        return Byte(self.value + value)

    def __sub__(self, target: Union["Byte", int]) -> "Byte":
        value: int = target.value if type(target) is Byte else target
        return Byte(self.value - value)


class Color:
    def __init__(self, color: str | tuple[int, int, int]):
        if type(color) is tuple:
            self.red = Byte(color[0])
            self.green = Byte(color[1])
            self.blue = Byte(color[2])
        else:
            color_code = str(color).replace("#", "")
            self.red = Byte.from_str(color_code[0:2])
            self.green = Byte.from_str(color_code[2:4])
            self.blue = Byte.from_str(color_code[4:6])

    @staticmethod
    def zip_rgb(*args: "Color") -> tuple[Bytes, Bytes, Bytes]:
        r, g, b = [], [], []
        for i in args:
            r.append(i.red)
            g.append(i.green)
            b.append(i.blue)
        return (r, g, b)

    @staticmethod
    def mean(colors: list["Color"]) -> "Color":
        red, green, blue = 0, 0, 0
        length = len(colors)
        for c in colors:
            red += c.red.as_int()
            green += c.green.as_int()
            blue += c.blue.as_int()
        return Color((red / length, green / length, blue / length))

    @staticmethod
    def invert(color: "Color") -> "Color":
        return Color(
            (
                (Byte(255) - color.red).as_int(),
                (Byte(255) - color.green).as_int(),
                (Byte(255) - color.blue).as_int(),
            )
        )

    @staticmethod
    def make_sequence(
        first_color: "Color", last_color: "Color", length: int
    ) -> list["Color"]:
        (red, green, blue) = Color.zip_rgb(first_color, last_color)
        red = fill_sequence(red[0].as_int(), red[1].as_int(), length)
        green = fill_sequence(green[0].as_int(), green[1].as_int(), length)
        blue = fill_sequence(blue[0].as_int(), blue[1].as_int(), length)
        return [Color(rgb) for rgb in zip(red, green, blue)]

    @staticmethod
    def derive_randomly(base_color: "Color", dev_level: float) -> "Color":
        [max_range, min_range] = [(5, 255), (0, 220)]
        [red, green, blue] = [
            random_deviation(base_color.red.as_int(), dev_level, min_range, max_range),
            random_deviation(
                base_color.green.as_int(), dev_level, min_range, max_range
            ),
            random_deviation(base_color.blue.as_int(), dev_level, min_range, max_range),
        ]
        return Color((red, green, blue))

    def __repr__(self) -> str:
        return f"Color<R={self.red};G={self.green};B={self.blue}>"

    def __str__(self) -> str:
        return f"#{self.red}{self.green}{self.blue}"

    def __add__(self, value: "Color") -> "Color":
        return Color(
            self.red + value.red, self.green + value.green, self.blue + value.blue
        )

    def __sub__(self, value: "Color") -> "Color":
        return Color(
            self.red - value.red, self.green - value.green, self.blue - value.blue
        )
