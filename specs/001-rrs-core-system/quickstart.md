# Quickstart: Core Re-RedScript System

## Installation

```bash
pip install rrs-core
# Dependencies: litemapy, ursina
```

## Creating Your First Module

```python
from rrs.core.block import Block
from rrs.core.module import Module
from rrs.io.exporter import rrs_export
from rrs.core.assertion import rrs_assert

# 1. Define a simple module function
def MakePillar(x, y, z, height):
    pillar = Module("Pillar", pos=(x, y, z))
    for i in range(height):
        # Create blocks relative to the pillar module (0, i, 0)
        # Note: If pillar is at (10, 0, 10), this block is at (10, i, 10) absolute
        b = Block("minecraft:stone", pos=(0, i, 0))
        pillar.add(b)
    return pillar

# 2. Instantiate modules
p1 = MakePillar(0, 0, 0, 3)
p2 = MakePillar(2, 0, 0, 3)

# 3. Assert properties (Debugging)
# Check if the base of p1 is indeed at (0,0,0) locally? 
# Accessing children might be needed for deep inspection
# assert p1.pos == (0,0,0)

# 4. Export to Litematica
structure = Module("MyStructure")
structure.add(p1)
structure.add(p2)

rrs_export(structure, "twin_pillars")
print("Exported twin_pillars.litematic")
```

## Visualizing

```python
from rrs.viz.viewer import rrs_viewer

rrs_viewer(structure)
```
