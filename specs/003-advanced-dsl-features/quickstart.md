# Quickstart: Advanced RRS

## 1. Variables and Loops

```python
module Grid(size):
    for x in range(0, size):
        for z in range(0, size):
            # Checkerboard pattern
            if (x + z) % 2 == 0:
                Stone(pos=(x, 0, z))
            else:
                Piston(pos=(x, 0, z))
```

## 2. Functions and Imports

**math_utils.rrs**:
```python
def calc_height(x):
    return x * x
```

**main.rrs**:
```python
from math_utils import calc_height

module Parabola():
    for x in range(0, 10):
        y = calc_height(x)
        Stone(pos=(x, y, 0))
```

## 3. Explicit Module Control

```python
module Custom():
    m = Module()
    m.add(Stone(pos=(0,0,0)))
    return m
```

## 4. Converting Litematics

To edit an existing structure:

1. Convert it: `rrs convert my_house.litematic -o my_house.rrs`
2. Edit `my_house.rrs`.
3. Compile it back: `rrs compile my_house.rrs`
