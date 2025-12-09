# Standard Library Reference

The Re-RedScript Standard Library provides a collection of utility functions for geometric shape generation, path creation, and block randomization. These functions must be imported from the `std` module.

## Usage

```python
# Import specific functions
from std import Line, Path

# Or import everything
from std import *
```

## Return Values

All shape functions (`Line`, `Path`, etc.) return a **`Module`** object containing the generated blocks. You must explicitly add this module to your build using `add()`.

## Custom Blocks and Modules (Advanced)

Standard library functions accept more than just simple Block types. You can pass:

1.  **Block Types**: `Stone`, `Dirt`
2.  **String IDs**: `"minecraft:diamond_block"`
3.  **Weighted Palettes**: `Weighted({...})`
4.  **Module Factories**: A user-defined `module Name(pos):`. The function will call `Name(pos=...)` for each point.
5.  **Module Instances**: An existing `Module` object. It will be cloned and repositioned.
6.  **Custom Blocks (blocks.json)**: You can define your own block types in a `blocks.json` file in your project directory.

### Defining Custom Blocks
Create a `blocks.json` file in the same directory as your script (or the project root):
```json
{
    "SuperBlock": {
        "id": "mod:super_block",
        "defaults": {
            "power": 10,
            "variant": "red"
        }
    }
}
```
You can then use `SuperBlock` directly in your RRS scripts:
```python
add(SuperBlock(pos=(0,10,0)))
```

```python
# 1. String ID
Line(start, end, "minecraft:generic_block")

# 2. Module Factory
module Pillar(pos):
    Block("minecraft:stone", pos=pos)
    Block("minecraft:torch", pos=(pos[0], pos[1]+1, pos[2]))

Line(start, end, Pillar)

# 3. Module Instance
m = Module("MyPart")
m.add(Block("minecraft:glass"))
Line(start, end, m)
```

## Functions

### Line
Draws a line between two points using a 3D line algorithm.

```python
Line(start, end, block, thickness=1) -> Module
```

- **start**: `(x,y,z)` tuple.
- **end**: `(x,y,z)` tuple.
- **block**: Block type or `Weighted` object.
- **thickness**: Line thickness (default: 1).

### Path
Connects a list of points with lines.

```python
Path(points, block, thickness=1, closed=False, smooth=False) -> Module
```

- **points**: List of `(x,y,z)` tuples.
- **block**: Block type.
- **closed**: If `True`, connects the last point back to the first.
- **smooth**: If `True`, generates a smooth Catmull-Rom spline passing *through* the points.

### Bezier
Draws a cubic Bezier curve defined by a start point, two control points, and an end point.

```python
Bezier(start, c1, c2, end, block, segments=20, thickness=1) -> Module
```

- **start**, **end**: Anchors.
- **c1**, **c2**: Control points.
- **segments**: Resolution of the curve.

### Geometric Shapes

#### Cuboid
Draws a solid or hollow box.

```python
Cuboid(pos1, pos2, block, fill=False) -> Module
```

- **pos1**, **pos2**: Opposite corners.
- **fill**: If `True`, fills the interior. Else, generates a shell.

#### Sphere
Draws a sphere.

```python
Sphere(center, radius, block, fill=False) -> Module
```

- **radius**: Integer radius.

#### Cylinder
Draws a cylinder along an axis.

```python
Cylinder(base, radius, height, block, axis='y', fill=False) -> Module
```

- **axis**: `'x'`, `'y'`, or `'z'`.

## Utilities

### Weighted
Creates a block palette where blocks are chosen based on probability weights.

```python
Weighted({
    BlockType: Weight,
    ...
})
```

**Example:**
```python
from std import Line, Weighted

# Create a path with 80% Dirt and 20% Coarse Dirt
mix = Weighted({
    Dirt: 0.8,
    CoarseDirt: 0.2
})

l = Line((0,0,0), (10,0,0), mix)
add(l)
```
