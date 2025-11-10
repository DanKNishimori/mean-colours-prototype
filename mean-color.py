import re
from random import uniform


def clip(base, min_v, max_v):
	if base < min_v:
		return min_v
	elif base > max_v:
		return max_v
	else:
		return base

def byte(hex_num: int):
	num = hex(hex_num).replace('0x', '')
	return "0" + num if len(num) < 2 else num

def fill_sequence(n0: int|float, nf: int|float, l: int):
    form = lambda idx : n0 + (idx-1)*(nf-n0)/(l-1)
    return [int(form(i)) for i in range(1, l+1)]


def is_number(string: str):
    if string.count('.') > 1:
        return False
    return string.replace('.', '').isnumeric()

def porcentage_to_float(string: str, std_value=0.2):
	if "%" in string:
		value = string.replace('%', '')
		return float(value)/100 if is_number(value) else std_value
	else:
		return float(string) if is_number(string) else std_value

def random_deviation(target: int|float, dev_level: float, min_range=(0, 2**32), max_range=(0, 2**32)):
	min_v = clip(target*abs(dev_level-1), min_range[0], min_range[1])
	max_v = clip(target*abs(dev_level+1), max_range[0], max_range[1])
	return uniform(min_v, max_v)

class Color:
	def __init__(self, color: str) -> None:
		c = color.replace("#", "")
		self.red = int(c[0:2], 16)
		self.green = int(c[2:4], 16)
		self.blue = int(c[4:6], 16)
	
	def from_rgb(r: int, g: int, b: int):
		new_color = Color("#000000")
		new_color.red = int(r)
		new_color.green = int(g)
		new_color.blue = int(b)
		return new_color
	
	def zip_rgb(*args: 'Color') -> tuple[list[int], list[int], list[int]]:
		r, g, b = [], [], []
		for i in args:
			r.append(i.red)
			g.append(i.green)
			b.append(i.blue)
		return (r, g, b)

	def mean(colors: list['Color']):
		red = 0
		green = 0
		blue = 0
		num = len(colors)
		for c in colors:
			red += c.red
			green += c.green
			blue += c.blue
		return Color.from_rgb(red/num, green/num, blue/num)

	def invert(color: 'Color'):
		base = Color('#FFFFFF')
		return Color.from_rgb(
			abs(color.red - base.red),
			abs(color.green - base.green),
			abs(color.blue - base.blue)
		)
	
	def make_sequence(first_color: 'Color', last_color: 'Color', length):
		(red, green, blue) = Color.zip_rgb(first_color, last_color)
		red = fill_sequence(red[0], red[1], length)
		green = fill_sequence(green[0], green[1], length)
		blue = fill_sequence(blue[0], blue[1], length)
		return [Color.from_rgb(r, g, b) for (r,g,b) in zip(red, green, blue)]

	def randderive(base_color: 'Color', dev_level):
		[max_range, min_range] = [(5, 255), (0, 220)]
		[red, green, blue] = [
			random_deviation(base_color.red, dev_level, min_range, max_range),
			random_deviation(base_color.green, dev_level, min_range, max_range),
			random_deviation(base_color.blue, dev_level, min_range, max_range)
		]
		return Color.from_rgb(red, green, blue)

	def __repr__(self) -> str:
		return f"Color<R={self.red};G={self.green};B={self.blue}>"
	
	def __str__(self) -> str:
		return f"#{byte(self.red)}{byte(self.green)}{byte(self.blue)}"

	def __add__(self, value: 'Color') -> 'Color':
		return Color.from_rgb(self.red + value.red, self.green + value.green, self.blue + value.blue)
	
	def __sub__(self, value: 'Color') -> 'Color':
		return Color.from_rgb(self.red - value.red, self.green - value.green, self.blue - value.blue)
	

COLOR_PTN = re.compile(r"#?([a-fA-F0-9]{6})")

while True:
	colors = []
	num = 0
	cmd = input(">>> ")
	if cmd in ["mean", "m"]:
		while (new := re.match(COLOR_PTN, input(f"[{num}]> "))):
			colors.append(Color(new.group(1)))
			num += 1
		else:
			print(f"the mean is: {Color.mean(colors)}")
	elif cmd in ["sequence", "s"]:
		first = Color(input("[ 1st]> "))
		last = Color(input("[last]> "))
		length = int(input("[ len]> "))
		for color in Color.make_sequence(first, last, length):
			print(color)
	elif cmd in ['rd']:
		base = Color(input("[base]> "))
		deviation_level = porcentage_to_float(input("[devl]> "))
		print(Color.randderive(base, deviation_level))
	elif cmd in ['i', "in"]:
		base = Color(input("[base]> "))
		print(Color.invert(base))
	elif cmd == "" :
		continue
	elif cmd in ['e', 'q', 'quit', 'exit']:
		break
	else:
		print(f"\"{cmd}\" is not a command!")
	
	print()


# cor = Color("#410c88")
# deviation_level = 0.2
# for _ in range(65):
# 	cor = Color.randderive(cor, deviation_level)
# 	print(cor)
