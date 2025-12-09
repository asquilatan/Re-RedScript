import os
from rrs.core.block import Block
from rrs.core.module import Module
from rrs.io.exporter import rrs_export
from rrs.core.assertion import rrs_assert

# 1. Define a simple module function
def MakePillar(x, y, z, height):
    pillar = Module("Pillar", pos=(x, y, z))
    for i in range(height):
        # Create blocks relative to the pillar module (0, i, 0)
        b = Block("minecraft:stone", pos=(0, i, 0))
        pillar.add(b)
    return pillar

# 2. Instantiate modules
p1 = MakePillar(0, 0, 0, 3)
p2 = MakePillar(2, 0, 0, 3)

# 3. Assert properties
assert p1.pos == (0, 0, 0)

# 4. Export to Litematica
structure = Module("MyStructure")
structure.add(p1)
structure.add(p2)

output_file = "twin_pillars.litematic"
rrs_export(structure, output_file)
print(f"Exported {output_file}")

assert os.path.exists(output_file)
# Cleanup
os.remove(output_file)
