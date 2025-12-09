# Re-RedScript (RRS) Language Guide

Re-RedScript (RRS) is a domain-specific language for designing Minecraft redstone circuits and structures. It compiles to `.litematic` files for use with the Litematica mod.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Blocks](#blocks)
3. [Variables](#variables)
4. [Modules](#modules)
5. [Adding Blocks to Modules](#adding-blocks-to-modules)
6. [Control Flow](#control-flow)
7. [Functions](#functions)
8. [Importing](#importing)
9. [Exporting](#exporting)
10. [Assertions](#assertions)
11. [Simulation](#simulation)
12. [Operators](#operators)

---

## Quick Start

```python
# Define a simple module
module House(width, height):
    for x in range(width):
        Block("minecraft:oak_planks", pos=(x, 0, 0))
    for y in range(height):
        Block("minecraft:oak_log", pos=(0, y, 0))

# Create and export the module
my_house = House(5, 4)
export(my_house)
```

**Compile with:**
```bash
rrs compile my_script.rrs
```

---

## Blocks

### Built-in Block Types

RRS provides shorthand classes for common Minecraft blocks:

```python
# Shorthand syntax
Stone(pos=(0, 0, 0))
Piston(pos=(1, 0, 0), facing="up")
Repeater(pos=(2, 0, 0), facing="north", delay=2)
Observer(pos=(3, 0, 0), facing="south")
RedstoneWire(pos=(4, 0, 0))
RedstoneTorch(pos=(5, 0, 0))
```

### Generic Block Constructor

For any Minecraft block:

```python
Block("minecraft:diamond_block", pos=(0, 0, 0))
Block("minecraft:oak_log", pos=(1, 0, 0), axis="y")
Block("minecraft:lever", pos=(2, 0, 0), face="wall", facing="north")
```

### Block Properties

Blocks accept keyword arguments for Minecraft block states:

| Property | Example Values | Used By |
|----------|---------------|---------|
| `pos` | `(x, y, z)` | All blocks |
| `facing` | `"north"`, `"south"`, `"east"`, `"west"`, `"up"`, `"down"` | Pistons, Observers, etc. |
| `delay` | `1`, `2`, `3`, `4` | Repeaters |
| `axis` | `"x"`, `"y"`, `"z"` | Logs, Pillars |
| `powered` | `true`, `false` | Rails, Wires |

---

## Variables

Variables store blocks, modules, or values for later use:

```python
# Store a block (does NOT auto-add to module)
my_block = Block("minecraft:stone", pos=(0, 0, 0))

# Store a value
height = 5
width = 10

# Use in expressions
total = width * height
```

> **Important**: Assigning a block to a variable does NOT automatically add it to the current module. Use `add()` to explicitly add it.

---

## Modules

Modules are reusable building blocks that group related blocks together.

### Defining Modules

```python
module Pillar(height):
    for y in range(height):
        Block("minecraft:stone", pos=(0, y, 0))

module Bridge(length, height):
    Pillar(height)                          # Left pillar
    Pillar(height, pos=(length - 1, 0, 0))  # Right pillar
    for x in range(length):
        Block("minecraft:oak_planks", pos=(x, height, 0))
```

### Instantiating Modules

```python
# Create a module instance
my_pillar = Pillar(5)

# Create with position offset
my_bridge = Bridge(10, 5, pos=(0, 0, 0))
```

### Returning Custom Modules

You can override what a module returns:

```python
module CustomBuilder():
    container = Module("MyContainer")
    container.add(Stone(pos=(0, 0, 0)))
    container.add(Stone(pos=(1, 0, 0)))
    return container

result = CustomBuilder()  # Returns "MyContainer" module
```

---

## Adding Blocks to Modules

### Auto-Add (Expression Statements)

Blocks used as expression statements are automatically added:

```python
module Example():
    Block("minecraft:stone", pos=(0, 0, 0))  # Auto-added
    Piston(pos=(1, 0, 0), facing="up")       # Auto-added
```

### No Auto-Add (Assignments)

Blocks assigned to variables are NOT automatically added:

```python
module Example():
    b = Block("minecraft:stone", pos=(0, 0, 0))  # NOT added
    # b is stored but not part of the module yet
```

### Explicit Add

Use `add()` to explicitly add blocks or modules:

```python
module Example():
    # Method 1: Add a stored block
    b = Block("minecraft:stone", pos=(0, 0, 0))
    add(b)
    
    # Method 2: Add inline
    add(Block("minecraft:dirt", pos=(0, 1, 0)))
    
    # Method 3: Add a nested module
    sub = SubModule()
    add(sub)
```

### Using += Operator

```python
module Example():
    container = Module("Container")
    container += Stone(pos=(0, 0, 0))
    container += Stone(pos=(1, 0, 0))
    return container
```

---

## Control Flow

### For Loops

```python
# Range with single argument
for i in range(5):        # 0, 1, 2, 3, 4
    Block("minecraft:stone", pos=(i, 0, 0))

# Range with start and end
for i in range(2, 6):     # 2, 3, 4, 5
    Block("minecraft:stone", pos=(i, 0, 0))

# Nested loops
for x in range(3):
    for z in range(3):
        Block("minecraft:stone", pos=(x, 0, z))
```

### Iterating Lists

```python
materials = ["minecraft:stone", "minecraft:dirt", "minecraft:sand"]
for i in range(3):
    Block(materials[i], pos=(i, 0, 0))
```

---

## Functions

Define reusable helper functions:

```python
def make_floor(width, depth, material):
    for x in range(width):
        for z in range(depth):
            Block(material, pos=(x, 0, z))
    return width * depth

module House():
    block_count = make_floor(5, 5, "minecraft:oak_planks")
    print(block_count)  # Outputs: 25
```

---

## Importing

### Import Entire Module

```python
import library

# Use imported modules
m = library.ImportedModule()
```

### Import Specific Items

```python
from library import Tower, Bridge

# Use directly
t = Tower(10)
b = Bridge(5)
```

### Import with Alias

```python
import my_long_library_name as lib

m = lib.SomeModule()
```

---

## Exporting

Use `export()` to mark modules for output to `.litematic`:

```python
module House():
    Block("minecraft:oak_planks", pos=(0, 0, 0))

# Create and export
h = House()
export(h)
```

**Multiple exports:**
```python
h1 = House()
h2 = House(pos=(10, 0, 0))
export(h1)
export(h2)
```

---

## Assertions

Use `assert()` to verify structures match expected configurations:

```python
module Expected():
    Piston(pos=(0, 0, 0), facing="north")

module Actual():
    Piston(pos=(0, 0, 0), facing="north")

e = Expected()
a = Actual()

# Assert structures match on specific properties
assert(a, e, "facing", "id")
print("Structures match!")
```

### Assert Parameters

```python
assert(actual, expected, *properties)
```

| Parameter | Description |
|-----------|-------------|
| `actual` | The structure to test (Module, Block, or list) |
| `expected` | The reference structure |
| `*properties` | Property names to check: `"id"`, `"facing"`, `"delay"`, etc. |

If no properties are specified, all properties are checked.

---

## Simulation

Simulate redstone behavior to verify circuit logic using the callback-based syntax.

### Basic Syntax

```python
m = TestModule()

Simulate((m, 500)):
    # Code runs within simulation context
    Trigger(m)
    ChangeState(m.lever, "powered", True)
    
    # Verify final state
    assert(m, expected_module, "pos")
```

### Parameters

| Part | Description |
|------|-------------|
| `m` | Module variable to simulate |
| `500` | Max game ticks (GT) to run (optional, default infinite) |
| Indented block | Body executed in simulation context |

### Module Trigger Blocks

Modules can define trigger blocks for initialization:

```python
module PistonDoor():
    lever = Lever(pos=(0,0,0), powered=False)
    piston = Piston(pos=(1,0,0), facing="up")
    
    trigger:
        ChangeState(lever, "powered", True)
```

### Simulation Functions

| Function | Description |
|----------|-------------|
| `Trigger(m)` | Invoke the module's trigger block |
| `ChangeState(block, property, value)` | Modify a block's state property |
| `assert(actual, expected, *props)` | Verify structures match |

### Block Access

Access blocks within a module:

```python
m.lever              # By registered name
m.get_block((0,0,0)) # By position
m["lever"]           # Dictionary-style
```

### Timing

| Component | Delay (GT) |
|-----------|------------|
| Redstone wire | 0 |
| Repeater 1-tick | 2 |
| Repeater 2-tick | 4 |
| Repeater 3-tick | 6 |
| Repeater 4-tick | 8 |
| Piston extend/retract | 3 |
| Observer pulse | 2 |

### Assert Behavior

| Usage | On Failure |
|-------|------------|
| `Simulate(...)` (not assigned) | Print error, exit code 1 |
| `result = Simulate(...)` | Returns `False` |

### Complete Example

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

print("Circuit verified!")
export(m)
```

---

## Operators

### Arithmetic

```python
x = 5 + 3    # 8
y = 10 - 2   # 8
z = 4 * 2    # 8
w = 16 / 2   # 8
```

### Comparison

```python
x == 5       # Equal
x != 3       # Not equal
x > 2        # Greater than
x < 10       # Less than
x >= 5       # Greater than or equal
x <= 5       # Less than or equal
```

### Augmented Assignment

```python
x = 0
x += 5       # x is now 5
```

---

## Built-in Functions

| Function | Description |
|----------|-------------|
| `range(n)` | Generate numbers 0 to n-1 |
| `range(start, end)` | Generate numbers start to end-1 |
| `print(value)` | Print to console |
| `abs(x)` | Absolute value |
| `floor(x)` | Round down |
| `sin(x)`, `cos(x)` | Trigonometry |
| `random()` | Random float 0-1 |
| `randint(a, b)` | Random integer a to b |

---

## Complete Example

```python
# tower.rrs - A parameterized watchtower

module Floor(size):
    for x in range(size):
        for z in range(size):
            Block("minecraft:stone_bricks", pos=(x, 0, z))

module Pillar(height):
    for y in range(height):
        Block("minecraft:oak_log", pos=(0, y, 0), axis="y")

module Watchtower(size, height):
    # Base floor
    Floor(size)
    
    # Corner pillars
    Pillar(height, pos=(0, 1, 0))
    Pillar(height, pos=(size-1, 1, 0))
    Pillar(height, pos=(0, 1, size-1))
    Pillar(height, pos=(size-1, 1, size-1))
    
    # Top floor
    Floor(size, pos=(0, height+1, 0))

# Build and export
tower = Watchtower(5, 8)
export(tower)
```

---

## CLI Reference

```bash
# Compile .rrs to .litematic
rrs compile input.rrs
rrs compile input.rrs -o output.litematic

# Convert .litematic to .rrs
rrs convert schematic.litematic
rrs convert schematic.litematic -o output.rrs
```
