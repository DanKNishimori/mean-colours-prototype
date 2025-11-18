import re
from color import Color, Colors


COLOR_PTN = re.compile(r"#?([a-fA-F0-9]{6})")


def percentage_to_float(str_percent: str) -> float:
    str_percent = str_percent.replace("%", "")
    return float(str_percent) if is_number(str_percent) else 0.0


def is_number(target: str) -> bool:
    has_multiple_dots = target.count(".") > 1
    free_dots_target = target.replace(".", "")
    return not has_multiple_dots and free_dots_target.isnumeric()


def mean():
    colors: Colors = []
    while new := re.match(COLOR_PTN, input(f"mean > ")):
        colors.append(Color(new.group(1)))
    print(f"the mean is: {Color.mean(colors)}")


def sequence():
    first = Color(input("[ 1st]> "))
    last = Color(input("[last]> "))
    length = int(input("[ len]> "))
    for color in Color.make_sequence(first, last, length):
        print(color)


def random_deviation():
    base = Color(input("[base]> "))
    deviation_level = percentage_to_float(input("[devl]> "))
    print(Color.derive_randomly(base, deviation_level))


def inversion():
    base = Color(input("[base]> "))
    print(Color.invert(base))


if __name__ == "__main__":
    while True:
        cmd = input(">>> ")
        if cmd in ["mean", "m"]:
            mean()
        elif cmd in ["sequence", "s"]:
            sequence()
        elif cmd in ["rd"]:
            random_deviation()
        elif cmd in ["i", "in"]:
            inversion()
        elif cmd == "":
            continue
        elif cmd in ["e", "q", "quit", "exit"]:
            break
        else:
            print(f'"{cmd}" is not a command!')

        print()
