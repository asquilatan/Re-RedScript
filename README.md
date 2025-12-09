# Re-RedScript (RRS)

**A Domain-Specific Language for Minecraft Redstone Engineering**

- **Syntax Highlighter:** [https://github.com/asquilatan/rrs-syntax-highlighter](https://github.com/asquilatan/rrs-syntax-highlighter)
- **Legacy Version (RedScript):** [https://github.com/asquilatan/RedScript](https://github.com/asquilatan/RedScript)

Re-RedScript (RRS) is a declarative DSL designed specifically for creating, testing, and validating Minecraft redstone contraptions. It compiles to `.litematic` files for use with the Litematica mod.

---

## Philosophy

### 🧱 Modularity First

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

### 🧪 Assertion-Driven Testing

RRS was specifically designed with testing in mind. The `assert()` function allows you to verify that contraptions match expected structures.

```python
# Verify your build matches the reference
assert(my_build, reference_build)

# Check only specific properties matter
assert(my_build, reference_build, "facing")

# Compare structure regardless of position (custom logic or flags if supported)
# Note: See docs for specific assertion flags
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/asquilatan/Re-RedScript.git
cd re-redscript

# Install in development mode
pip install -e .

# Verify installation
rrs --help
```

After installation, the `rrs` command is available globally.

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

### 3. Load in Minecraft

1. Install the [Litematica](https://www.curseforge.com/minecraft/mc-mods/litematica) mod.
2. Copy the `.litematic` file to `.minecraft/schematics/`.
3. Use Litematica to load and paste the schematic.

---

## CLI Reference

### Compile Command

```bash
rrs compile <file.rrs> [-o output.litematic]
```

| Option | Description |
|--------|-------------|
| `<file.rrs>` | Input RRS script file |
| `-o, --output` | Output file path (default: `<input>.litematic`) |

**Examples:**
```bash
# Basic compile
rrs compile door.rrs

# Custom output path
rrs compile door.rrs -o builds/3x3_door.litematic
```

---

## Language Reference

### Blocks

RRS provides shorthand classes for common Minecraft blocks and a generic `Block` constructor.

```python
# Shorthand syntax
Stone(pos=(0, 0, 0))
Piston(pos=(1, 0, 0), facing="up")
Repeater(pos=(2, 0, 0), facing="north", delay=2)

# Generic syntax
Block("minecraft:diamond_block", pos=(0, 0, 0))
```

**Common Properties:**
- `pos`: `(x, y, z)` tuple.
- `facing`: `"north"`, `"south"`, `"east"`, `"west"`, `"up"`, `"down"`.
- `delay`: `1`, `2`, `3`, `4`.

### Variables

Variables can store values or blocks. Note that assigning a block to a variable does **not** automatically add it to the module; you must use `add()`.

```python
height = 5
width = 10

# Block assignment (not added yet)
b = Block("minecraft:stone", pos=(0, 0, 0))
add(b) # Explicitly add
```

### Modules

Modules group blocks together.

```python
module Bridge(length):
    for x in range(length):
        Block("minecraft:oak_planks", pos=(x, 0, 0))

# Instantiate
Bridge(10)
```

### Control Flow

RRS supports `if`, `elif`, `else`, `while`, and `for` loops.

```python
for i in range(5):
    Stone(pos=(i, 0, 0))

if height > 10:
    print("Tall structure")
```

### Imports

Import modules from other `.rrs` files.

```python
import library
# Use: library.MyModule()

from library import MyModule
# Use: MyModule()
```

### Built-in Functions

- `range(n)`, `range(start, end)`
- `print(value)`
- `len(list)`, `append(list, item)`, `pop(list)`, `insert(list, index, item)`
- `str()`, `int()`, `float()`, `bool()`
- Math: `sin`, `cos`, `sqrt`, `pow`, `floor`, `ceil`, `round`, `abs`, `min`, `max`, `random`, `randint`
- Constants: `PI`, `E`

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

