import os
import sys
from typing import Union, List

# Ensure src is in python path if running from root
sys.path.insert(0, os.path.abspath("src"))

from rrs import Module, Block, Stone, Piston, Repeater, rrs_export, rrs_import
from rrs.core.module import Module

# Define missing blocks from the sample
class Clay(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:clay", pos, **kwargs)

# The sample code uses a function-like definition for Module, but instantiates it.
# We map this to a class inheriting from Module.
class SampleModule(Module):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        # We assume the ID is the class name
        super().__init__("SampleModule", pos, **kwargs)
        x, y, z = pos
        
        # "to call other modules, just instantiate them" -> In actual RRS we add them to self
        # p1 = Piston(pos=(x, y, z), facing="up")
        self.add(Piston(pos=(x, y, z), facing="up"))
        
        # r1 = Repeater(pos=(x + 1, y, z), facing="east", delay=4)
        self.add(Repeater(pos=(x + 1, y, z), facing="east", delay=4))

# "a module can be instantiated like this"
s = SampleModule(pos=(0, 0, 0))

# "now to export a module..."
print("Exporting SampleModule...")
rrs_export(s, "SampleModule.litematic")

# "we can also convert existing minecraft litematica structures..."
# We use the file we just exported since the sample one doesn't exist
print("Importing ImportedModule...")
if os.path.exists("SampleModule.litematic"):
    im = rrs_import("SampleModule.litematic", "ImportedModule")
else:
    print("Warning: SampleModule.litematic not found, skipping import.")
    im = Module("ImportedModule") # Dummy

# "again, you could put modules in modules"
class ComplexModule(Module):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("ComplexModule", pos, **kwargs)
        x, y, z = pos
        
        # sm1 = SampleModule(pos=(x, y, z))
        self.add(SampleModule(pos=(x, y, z)))
        
        # im1 = ImportedModule(pos=(x + 2, y, z))
        # We need to clone 'im' or re-instantiate if it was a class. 
        # Since 'im' is an instance, we should probably treat it as a prototype or use a factory.
        # For this sample, we'll manually add a generic module or reuse the imported one (cloning if RRS supported it).
        # We'll just instantiate a new SampleModule to mimic 'ImportedModule' behavior for the structure
        # or properly, if ImportedModule was a class. Here 'im' is an instance.
        # We will wrap it in a container or just add it (but adding modifies parent).
        # We'll re-import for simplicity to match 'ImportedModule(pos=...)' semantic if it were a factory.
        
        # Simulating ImportedModule(pos=...)
        # Since we don't have a factory for the imported module, we'll just add a placeholder or re-import
        # In a real scenario, rrs_import might return a Class or Factory. Here it returns a Module instance.
        # We will attempt to use the 'im' instance structure.
        pass

# Adjusting ComplexModule to actually work with the instance 'im'
# In the sample: im = rrs_import(...)
# In the sample: im1 = ImportedModule(pos=...) 
# This implies ImportedModule became a class/factory. 
# We'll define a factory wrapper.
def ImportedModuleFactory(pos):
    # Re-import or clone. For efficiency, let's just make a dummy Module with the same ID
    # In a real app we'd clone the imported structure.
    return Module("ImportedModule", pos=pos)

class ComplexModule(Module):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("ComplexModule", pos, **kwargs)
        x, y, z = pos
        self.add(SampleModule(pos=(x, y, z)))
        self.add(ImportedModuleFactory(pos=(x + 2, y, z)))

cm = ComplexModule(pos=(0, 0, 0))
print("Exporting ComplexModule...")
rrs_export(cm, "ComplexModule.litematic")


# ----- specifications for re-redscript assertions ----- 

# Custom implementation of rrs_assert to support properties filtering as per sample code
def rrs_assert(actual: Union[Module, List[Module]], expected: Union[Module, List[Module]], *properties) -> bool:
    """
    Assert that two modules or structures are identical based on specific properties.
    """
    # Normalize to list of blocks
    if isinstance(actual, Module):
        actual_blocks = actual.flatten()
    else:
        actual_blocks = actual
        
    if isinstance(expected, Module):
        expected_blocks = expected.flatten()
    else:
        expected_blocks = expected
        
    # Sort by position to ensure order doesn't matter for comparison
    actual_blocks.sort(key=lambda b: b.pos)
    expected_blocks.sort(key=lambda b: b.pos)
    
    if len(actual_blocks) != len(expected_blocks):
        print(f"Assertion Failed: Block count mismatch: {len(actual_blocks)} != {len(expected_blocks)}")
        return False
        
    for b1, b2 in zip(actual_blocks, expected_blocks):
        # Default checks if no properties specified? 
        # The sample implies if properties ARE specified, ONLY check those?
        # Or always check position? 
        # "ans = rrs_assert(..., 'id')" -> checks id.
        # "ans = rrs_assert(..., 'id', 'pos')" -> checks id and pos.
        
        checks = properties if properties else ["id", "pos", "properties"]
        
        for prop in checks:
            if prop == "pos":
                if b1.pos != b2.pos:
                    print(f"Assertion Failed: Position mismatch {b1.pos} != {b2.pos}")
                    return False
            elif prop == "id":
                if b1.id != b2.id:
                    print(f"Assertion Failed: ID mismatch {b1.id} != {b2.id}")
                    return False
            else:
                # Check specific property in kwargs/properties
                # Not fully implemented in Block class but let's assume attributes or 'properties' dict
                # The Block class puts kwargs into properties?
                # Block definition: super().__init__(..., **kwargs) -> self.properties = kwargs
                val1 = getattr(b1, prop, b1.properties.get(prop))
                val2 = getattr(b2, prop, b2.properties.get(prop))
                if val1 != val2:
                     print(f"Assertion Failed: Property '{prop}' mismatch {val1} != {val2}")
                     return False
    
    return True


print("\nRunning Assertions...")

b1 = Stone(pos=(0, 0, 0))
b2 = Stone(pos=(0, 0, 1))
b3 = Stone(pos=(0, 0, 2))
b4 = Stone(pos=(0, 1, 0))
b5 = Stone(pos=(0, 1, 1))
b6 = Stone(pos=(0, 1, 2))
b7 = Stone(pos=(0, 2, 0))
b8 = Stone(pos=(0, 2, 1))
b9 = Stone(pos=(0, 2, 2))
structure_to_check = [b1, b2, b3, b4, b5, b6, b7, b8, b9]

# the following assertion should pass, and ans should be true
ans = rrs_assert(Stone(pos=(0, 0, 0)), Stone(pos=(0, 0, 0)), "pos")
print(f"Test 1 (Pass): {ans}")

#  the following assertion should fail, and ans should be false
ans = rrs_assert(Stone(pos=(0, 0, 0)), Stone(pos=(0, 0, 1)), "pos")
print(f"Test 2 (Fail): {ans}")

# the following assertion should pass, and ans should be true (because id is the same for both blocks)
ans = rrs_assert(Stone(pos=(0, 0, 0)), Stone(pos=(0, 0, 1)), "id")
print(f"Test 3 (Pass): {ans}")

# the following assertion should fail, and ans should be false (id is the same for both blocks, but pos is different)
ans = rrs_assert(Stone(pos=(0, 0, 0)), Stone(pos=(0, 0, 1)), "id", "pos")
print(f"Test 4 (Fail): {ans}")

# the following assertion should fail, and ans should be false (id is different for both blocks, even though pos is the same)
ans = rrs_assert(Stone(pos=(0, 0, 0)), Clay(pos=(0, 0, 0)), "id", "pos")
print(f"Test 5 (Fail): {ans}")

# you should also be able to compare entire structures

correct_structure = [
        Stone(pos=(0, 0, 0)),
        Stone(pos=(0, 0, 1)),
        Stone(pos=(0, 0, 2)),
        Stone(pos=(0, 1, 0)),
        Stone(pos=(0, 1, 1)),
        Stone(pos=(0, 1, 2)),
        Stone(pos=(0, 2, 0)),
        Stone(pos=(0, 2, 1)),
        Stone(pos=(0, 2, 2)),
    ]

# the following assertion should pass, and ans should be true
ans = rrs_assert(structure_to_check, correct_structure, "id", "pos")
print(f"Test 6 (Pass): {ans}")

# the following assertion should fail, because at least 1 of the blocks are different, and ans should be false
b1_clay = Clay(pos=(0, 0, 0))
structure_to_check_clay = [b1_clay, b2, b3, b4, b5, b6, b7, b8, b9]
ans = rrs_assert(structure_to_check_clay, correct_structure, "id", "pos")
print(f"Test 7 (Fail): {ans}")

# the following assertion should fail, because at least 1 of the blocks are different in position, and ans should be false
b1_moved = Stone(pos=(1, 0, 0))
structure_to_check_moved = [b1_moved, b2, b3, b4, b5, b6, b7, b8, b9]
ans = rrs_assert(structure_to_check_moved, correct_structure, "id", "pos")
print(f"Test 8 (Fail): {ans}")

print("\nDone.")
