from random import uniform


def clip(base: int | float, min_v: int | float, max_v: int | float) -> int | float:
    if base < min_v:
        return min_v
    elif base > max_v:
        return max_v
    return base


def to_byte(hex_num: int) -> str:
    num = hex(hex_num).replace("0x", "")
    return "0" + num if len(num) < 2 else num


def fill_sequence(n0: int | float, nf: int | float, l: int) -> list[int]:
    form = lambda idx: n0 + (idx - 1) * (nf - n0) / (l - 1)
    return [int(form(i)) for i in range(1, l + 1)]


def random_deviation(
    target: int | float, dev_level: float, min_range=(0, 2**8), max_range=(0, 2**8)
) -> float:
    min_v = clip(target * abs(dev_level - 1), min_range[0], min_range[1])
    max_v = clip(target * abs(dev_level + 1), max_range[0], max_range[1])
    return uniform(min_v, max_v)


class Color:
    def __init__(self, color: str | tuple[int, int, int]):
        if type(color) is tuple:
            self.red = int(color[0])
            self.green = int(color[1])
            self.blue = int(color[2])
        else:
            color_code = color.replace("#", "")
            self.red = int(color_code[0:2], 16)
            self.green = int(color_code[2:4], 16)
            self.blue = int(color_code[4:6], 16)

    @staticmethod
    def zip_rgb(*args: "Color") -> tuple[list[int], list[int], list[int]]:
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
            red += c.red
            green += c.green
            blue += c.blue
        return Color((red / length, green / length, blue / length))

    @staticmethod
    def invert(color: "Color") -> "Color":
        base = Color("#FFFFFF")
        return Color(
            (
                abs(color.red - base.red),
                abs(color.green - base.green),
                abs(color.blue - base.blue),
            )
        )

    @staticmethod
    def make_sequence(
        first_color: "Color", last_color: "Color", length: int
    ) -> list["Color"]:
        (red, green, blue) = Color.zip_rgb(first_color, last_color)
        red = fill_sequence(red[0], red[1], length)
        green = fill_sequence(green[0], green[1], length)
        blue = fill_sequence(blue[0], blue[1], length)
        return [Color(rgb) for rgb in zip(red, green, blue)]

    @staticmethod
    def derive_randomly(base_color: "Color", dev_level: float) -> "Color":
        [max_range, min_range] = [(5, 255), (0, 220)]
        [red, green, blue] = [
            random_deviation(base_color.red, dev_level, min_range, max_range),
            random_deviation(base_color.green, dev_level, min_range, max_range),
            random_deviation(base_color.blue, dev_level, min_range, max_range),
        ]
        return Color((red, green, blue))

    def __repr__(self) -> str:
        return f"Color<R={self.red};G={self.green};B={self.blue}>"

    def __str__(self) -> str:
        return f"#{to_byte(self.red)}{to_byte(self.green)}{to_byte(self.blue)}"

    def __add__(self, value: "Color") -> "Color":
        return Color(
            self.red + value.red, self.green + value.green, self.blue + value.blue
        )

    def __sub__(self, value: "Color") -> "Color":
        return Color(
            self.red - value.red, self.green - value.green, self.blue - value.blue
        )
