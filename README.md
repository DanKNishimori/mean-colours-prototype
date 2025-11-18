# Mean Colours (prototype)
This is an script I made for help me with a few problems related to colors.

## Commands
- `mean` or `m`
    Stores a list of colors and return the mean color.

```
>>> m
mean > #00ff00
mean > #0000ff
mean >
the mean is: #007f7f

>>>
```

- `sequence` or `s`
    Takes the first and last colors, then—with a given length—a list of hex colors is generated.

```
>>> s
[ 1st]> #00ff00
[last]> #0000ff
[ len]> 6
#00ff00
#00cc33
#009966
#006699
#0033cc
#0000ff

>>>
```

- `in` or `i` (inversion)
    Inverts a given base color.

```  
>>> i
[base]> #00ff00
#ff00ff

>>>
```

- `rd` (random deviation)
    Takes a given base color and changes randomly it with a `devl` (deviation level).
    (Malfunctioning)

```
>>> rd
[base]> #00ff00
[devl]> 5
#00de00

>>>
```

- `quit`, `exit`, `e` or `q`
    Exits the program.

```
>>> e

```
