# Re-RedScript (RRS)

**A Domain-Specific Language for Minecraft Redstone Engineering**

- **Syntax Highlighter:** [https://github.com/asquilatan/rrs-syntax-highlighter](https://github.com/asquilatan/rrs-syntax-highlighter)
- **Legacy Version (RedScript):** [https://github.com/asquilatan/RedScript](https://github.com/asquilatan/RedScript)

Re-RedScript (RRS) is a declarative DSL designed specifically for creating, testing, and validating Minecraft redstone contraptions. It compiles to `.litematic` files for use with the Litematica mod.

---

## Philosophy

### Modularity First

RRS is built around the concept of **modules**: reusable, parameterized building blocks that can be composed into complex contraptions. Instead of placing blocks one-by-one, you define modules once and instantiate them anywhere.

```python
module Pillar(x, y, z, height):
    for i in range(height):
        Stone(pos=(x, y + i, z))
    Glowstone(pos=(x, y + height, z))

# Use it multiple times
Pillar(0, 0, 0, 5)
Pillar(4, 0, 0, 8)
Pillar(8, 0, 0, 3)
```

### Assertion-Driven Testing

RRS was specifically designed with testing in mind. The `assert()` function allows you to verify that contraptions match expected structures.

```python
# Verify your build matches the reference
assert(my_build, reference_build)

# Check only specific properties matter
assert(my_build, reference_build, "facing")
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/asquilatan/Re-RedScript.git
cd re-redscript

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Verify installation
rrs --help
```

---

## Quick Start

### 1. Create a Script

Create a file called `my_contraption.rrs`:

```python
# Define a simple component
module TFlipFlop(x, y, z):
    Piston(pos=(x, y, z), facing="up")
    RedstoneBlock(pos=(x, y + 1, z))
    Observer(pos=(x + 1, y, z), facing="west")
    Repeater(pos=(x + 2, y, z), facing="west", delay=1)

# Instantiate it
TFlipFlop(0, 0, 0)
```

### 2. Compile to Litematic

```bash
rrs compile my_contraption.rrs
```

This creates `my_contraption.litematic` in the same directory.

---

## Standard Library

RRS includes a robust standard library for geometry and image processing.

### Import Syntax

```python
import std.line as line
import std.figure as fig
import std.img as img
```

### Geometry (`std.line`)

Functions for drawing lines and paths.

```python
# Draw a Line
l = line.Line((0,0,0), (10,5,0), Stone)
add(l)

# Draw a Bezier curve
b = line.Bezier((0,0,0), (5,10,0), (15,10,0), (20,0,0), GoldBlock)
add(b)

# Draw a Path (optionally smooth)
p = line.Path([(0,0,0), (5,0,5), (10,0,0)], DiamondBlock, smooth=True)
add(p)
```

### Shapes (`std.figure`)

Functions for solid shapes.

```python
# Draw a hollow Sphere
s = fig.Sphere((0,10,0), 5, Glass)
add(s)

# Draw a filled Cuboid
c = fig.Cuboid((0,0,0), (5,5,5), Stone, fill=True)
add(c)
```

### Image Processing (`std.img`)

Convert images into Minecraft blocks. RRS automatically maps pixels to a colorful palette of blocks.

```python
# Basic import (horizontal, flat)
m = img.ConvertPicture("logo.png")
add(m)

# Vertical billboard
m2 = img.ConvertPicture("logo.png", vertical=True)
add(m2)

# Resizing
m3 = img.ConvertPicture("logo.png", length=50, width=50)
add(m3)

# 3D Heightmap Generation
# Uses pixel brightness to determine height
terrain = img.ConvertPicture("heightmap.png", height=20, heightmap=True)
add(terrain)
```

---

## CLI Reference

### Compile Command

```bash
rrs compile <file.rrs> [-o output.litematic]
```

### Convert Command

```bash
rrs convert <schematic.litematic> [-o output.rrs] [--module-name MODULE_NAME]
```

---

## Language Reference

### Blocks

RRS provides shorthand classes for common Minecraft blocks and a generic `Block` constructor.

```python
# Shorthand syntax
Stone(pos=(0, 0, 0))
Piston(pos=(1, 0, 0), facing="up")

# Generic syntax
Block("minecraft:diamond_block", pos=(0, 0, 0))
```

### Custom Blocks
You can define your own blocks in a `blocks.json` file in your project root.

### Variables

Variables can store values or blocks. Note that assigning a block to a variable does **not** automatically add it to the module; you must use `add()`.

```python
b = Block("minecraft:stone", pos=(0, 0, 0))
add(b) # Explicitly add
```

### Control Flow

RRS supports `if`, `elif`, `else`, `while`, and `for` loops.

### Built-in Functions

- Math: `sin`, `cos`, `sqrt`, `random`, etc.
- Lists: `len`, `append`, `pop`, `insert`
- `range`, `print`, `assert`

---

## Assertions & Simulation

RRS supports simulation and assertion-based testing.

```python
module Circuit():
    lever = Lever(pos=(0,0,0), powered=False)
    piston = Piston(pos=(1,0,0), facing="up")

module Expected():
    lever = Lever(pos=(0,0,0), powered=True)
    piston = Piston(pos=(1,0,0), facing="up", extended=True)

m = Circuit()
e = Expected()

Simulate((m, 100)):
    ChangeState(m.lever, "powered", True)
    assert(m, e)
```

---

## License

MIT License - See LICENSE file for details.
