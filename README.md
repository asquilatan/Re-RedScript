# Re-RedScript (RRS)

**A Domain-Specific Language for Minecraft Redstone Engineering**

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
assert(my_build, reference_build, properties=["facing"])

# Compare structure regardless of position
assert(my_build, reference_build, relative_pos=True)
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
# Define a simple T-flip-flop component
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

1. Install the [Litematica](https://www.curseforge.com/minecraft/mc-mods/litematica) mod
2. Copy the `.litematic` file to `.minecraft/schematics/`
3. Use Litematica to load and paste the schematic

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

### Modules

Modules are the core building block of RRS. They encapsulate a collection of blocks and can be parameterized.

```python
module ModuleName(param1, param2, ...):
    # Block placements go here
    Block(pos=(param1, param2, 0))
```

**Instantiation:**
```python
ModuleName(10, 20)
```

### Blocks

Built-in block types with their properties:

| Block | Properties | Example |
|-------|------------|---------|
| `Stone` | `pos` | `Stone(pos=(0,0,0))` |
| `Piston` | `pos`, `facing` | `Piston(pos=(0,0,0), facing="up")` |
| `Repeater` | `pos`, `facing`, `delay` | `Repeater(pos=(0,0,0), facing="north", delay=4)` |
| `Observer` | `pos`, `facing` | `Observer(pos=(0,0,0), facing="east")` |
| `GoldBlock` | `pos` | `GoldBlock(pos=(0,0,0))` |
| `DiamondBlock` | `pos` | `DiamondBlock(pos=(0,0,0))` |
| `EmeraldBlock` | `pos` | `EmeraldBlock(pos=(0,0,0))` |
| `IronBlock` | `pos` | `IronBlock(pos=(0,0,0))` |
| `RedstoneBlock` | `pos` | `RedstoneBlock(pos=(0,0,0))` |
| `LapisBlock` | `pos` | `LapisBlock(pos=(0,0,0))` |
| `Glowstone` | `pos` | `Glowstone(pos=(0,0,0))` |
| `SeaLantern` | `pos` | `SeaLantern(pos=(0,0,0))` |
| `Block` | `id`, `pos`, `**properties` | `Block("minecraft:oak_planks", pos=(0,0,0))` |

**Facing Values:** `"north"`, `"south"`, `"east"`, `"west"`, `"up"`, `"down"`

**Delay Values:** `1`, `2`, `3`, `4` (redstone ticks)

### Variables

```python
height = 10
spacing = 2
base_x = 100

module Tower(x, y, z):
    for i in range(height):
        Stone(pos=(x, y + i * spacing, z))
```

### Functions

Functions perform calculations and return values:

```python
def calculate_offset(index):
    return index * 3 + 1

module Pattern(x, y, z):
    for i in range(5):
        offset = calculate_offset(i)
        Stone(pos=(x + offset, y, z))
```

### Loops

```python
# Range-based loop
for i in range(10):
    Stone(pos=(i, 0, 0))

# Nested loops for grids
for x in range(5):
    for z in range(5):
        Stone(pos=(x, 0, z))
```

### Imports

Import modules from other `.rrs` files:

```python
# Import entire module namespace
import library

# Use with namespace prefix
library.MyComponent(0, 0, 0)

# Import specific modules directly
from library import MyComponent, AnotherComponent

# Use directly
MyComponent(0, 0, 0)
```

### Built-in Functions

| Function | Description | Example |
|----------|-------------|---------|
| `range(n)` | Generate sequence 0 to n-1 | `for i in range(5)` |
| `print(msg)` | Debug output | `print("Building...")` |
| `sin(x)` | Sine (radians) | `sin(PI / 2)` |
| `cos(x)` | Cosine (radians) | `cos(angle)` |
| `floor(x)` | Round down to integer | `floor(3.7)` → `3` |
| `abs(x)` | Absolute value | `abs(-5)` → `5` |
| `random()` | Random float 0.0-1.0 | `random()` |
| `randint(a, b)` | Random integer a to b | `randint(1, 10)` |

### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `PI` | 3.14159... | Mathematical pi |

---

## Assertions

The `assert()` function is the heart of RRS testing. It compares two modules and raises an error if they don't match.

### Basic Usage

```python
module Expected(x, y, z):
    Piston(pos=(x, y, z), facing="up")
    Repeater(pos=(x + 1, y, z), facing="east", delay=2)

module MyBuild(x, y, z):
    Piston(pos=(x, y, z), facing="up")
    Repeater(pos=(x + 1, y, z), facing="east", delay=2)

# These should match exactly
expected = Expected(0, 0, 0)
actual = MyBuild(0, 0, 0)
assert(actual, expected)
```

### Assertion Options

| Parameter | Type | Description |
|-----------|------|-------------|
| `relative_pos` | `bool` | Normalize positions to origin before comparing |
| `ignore_pos` | `bool` | Ignore positions entirely (check composition only) |
| `properties` | `list` | Only check specific properties (e.g., `["facing"]`) |

**Examples:**

```python
# Compare structures regardless of where they're placed
assert(build_a, build_b, relative_pos=True)

# Only check that facing directions match
assert(build_a, build_b, properties=["facing"])

# Check block composition only (ignore all positions)
assert(build_a, build_b, ignore_pos=True)
```

### Error Messages

When assertions fail, you get detailed error messages:

```
AssertionError: Block #2 (minecraft:piston) property 'facing' mismatch: up != down
```

---

## Example: Testing a 3x3 Piston Door

```python
# reference.rrs - The known-good door design
module PistonDoor3x3(x, y, z):
    # Bottom layer
    Piston(pos=(x, y, z), facing="up")
    Piston(pos=(x + 1, y, z), facing="up")
    Piston(pos=(x + 2, y, z), facing="up")
    
    # Middle layer
    Piston(pos=(x, y + 1, z), facing="east")
    Piston(pos=(x + 2, y + 1, z), facing="west")
    
    # Top layer
    Piston(pos=(x, y + 2, z), facing="down")
    Piston(pos=(x + 1, y + 2, z), facing="down")
    Piston(pos=(x + 2, y + 2, z), facing="down")
    
    # Timing circuit
    Repeater(pos=(x + 3, y, z), facing="west", delay=2)
    Repeater(pos=(x + 3, y + 1, z), facing="west", delay=4)
    Observer(pos=(x + 3, y + 2, z), facing="west")

# test_door.rrs - Test your implementation
from reference import PistonDoor3x3

module MyDoorImplementation(x, y, z):
    # Your implementation here...
    pass

# Verify it matches the reference
reference = PistonDoor3x3(0, 0, 0)
my_door = MyDoorImplementation(0, 0, 0)

# This will pass if your door matches the reference
assert(my_door, reference)
print("Door implementation verified!")
```

---

## Project Structure

```
my-project/
├── components/
│   ├── pistons.rrs      # Piston utilities
│   ├── timing.rrs       # Timing circuits
│   └── doors.rrs        # Door modules
├── tests/
│   ├── test_pistons.rrs
│   └── test_doors.rrs
└── main.rrs             # Main build script
```

**main.rrs:**
```python
from components.doors import FlushDoor3x3
from components.timing import ObserverClock

module MyBase(x, y, z):
    FlushDoor3x3(x, y, z)
    ObserverClock(x + 10, y, z)

MyBase(0, 64, 0)
```

---

## Best Practices

### 1. Use Descriptive Module Names
```python
# Good
module StickyPistonExtender(x, y, z):

# Avoid
module SPE(x, y, z):
```

### 2. Parameterize Everything
```python
# Good - reusable with any height
module Tower(x, y, z, height):
    for i in range(height):
        Stone(pos=(x, y + i, z))

# Avoid - hardcoded values
module Tower(x, y, z):
    for i in range(5):  # Magic number
        Stone(pos=(x, y + i, z))
```

### 3. Write Tests for Complex Contraptions
```python
# Always have a reference implementation
module ReferenceDoor(x, y, z):
    # Known-good implementation

# Test your optimized version against it
module OptimizedDoor(x, y, z):
    # Your optimized version

assert(OptimizedDoor(0,0,0), ReferenceDoor(0,0,0), relative_pos=True)
```

### 4. Organize with Imports
```python
# Split large projects into logical files
from timing import PulseExtender, EdgeDetector
from pistons import DoublePistonExtender
```

---

## Troubleshooting

### "Unknown block or module: X"
- Check spelling of block/module name
- Ensure the module is defined before use
- For imports, verify the file exists

### "Block count mismatch"
- Your build has more/fewer blocks than expected
- Check for missing or duplicate block placements

### "Block position mismatch"
- Positions don't align — check your coordinate math
- Use `relative_pos=True` if absolute positions don't matter

### "Block property mismatch"
- A property like `facing` or `delay` differs
- Use `properties=["facing"]` to check specific properties only

---

## License

MIT License - See LICENSE file for details.

---

