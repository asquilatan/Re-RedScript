# in re-redscript, the smallest quantum is a module
# each module has properties that define its behavior and appearance
# these should be based on the actual minecraft block properties

# defining some sample blocks, each with their own properties
# (this will be placed in a separate massive file in the actual implementation)
blocks = {
    "Piston": {
        "id": "minecraft:piston",
        "size": (1, 1, 1),
        "pos": (0, 0, 0),
        "powered": False,
        "facing": "north",
        "texture": "src/assets/blocks/piston.png",
    },
    "Repeater": {
        "id": "minecraft:repeater",
        "size": (1, 1, 1),
        "pos": (0, 0, 0),
        "powered": False,
        "facing": "north",
        "delay": 1,
        "texture": "src/assets/blocks/repeater.png",
    },
}

# a module can be defined as a function that combines smaller modules
def SampleModule(self, x, y, z):
    
    # to call other modules, just instantiate them
    p1 = Piston(pos=(x, y, z), facing="up")
    r1 = Repeater(pos=(x + 1, y, z), facing="east", delay=4)

# a module can be instantiated like this
s = SampleModule(pos=(0, 0, 0))

# each module can have its own parameters and default values
# default blocks such as Pistons, Repeaters, and other minecraft blocks are predefined!
def Piston(self):
    # it should automatically use the properties defined in the blocks dictionary
    pass

def Repeater(self):
    pass

# now to export a module, we can use the export function. this should take in the module instance and an output name
rrs_export(s, "SampleModule")

# we can also convert existing minecraft litematica structures into re-redscript modules. 
# this would act as if we defined the module ourselves. ImportedModule would be the name of the module created from the litematic file
im = rrs_import("src/assets/structures/sample_structure.litematic", "ImportedModule")

# we should also be able to visualize modules in a 3d viewer. 
# This first converts it into a litematic structure, then opens it in the viewer. 
rrs_viewer(im)

# again, you could put modules in modules
def ComplexModule(self, x, y, z):
    sm1 = SampleModule(pos=(x, y, z))
    im1 = ImportedModule(pos=(x + 2, y, z))

cm = ComplexModule(pos=(0, 0, 0))
# this outputs ComplexModule.litematic using a converter
rrs_export(cm, "ComplexModule")

# ----- specifications for re-redscript assertions -----
# to help with debugging, we can have an assertion function that checks if two modules are the same based on certain properties
# To guarantee that the AI can debug this, we can assert that specific modules contain certain properties
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

#  the following assertion should fail, and ans should be false
ans = rrs_assert(Stone(pos=(0, 0, 0)), Stone(pos=(0, 0, 1)), "pos")

# the following assertion should pass, and ans should be true (because id is the same for both blocks)
ans = rrs_assert(Stone(pos=(0, 0, 0)), Stone(pos=(0, 0, 1)), "id")

# the following assertion should fail, and ans should be false (id is the same for both blocks, but pos is different)
ans = rrs_assert(Stone(pos=(0, 0, 0)), Stone(pos=(0, 0, 1)), "id", "pos")

# the following assertion should fail, and ans should be false (id is different for both blocks, even though pos is the same)
ans = rrs_assert(Stone(pos=(0, 0, 0)), Clay(pos=(0, 0, 0)), "id", "pos")

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

# the following assertion should fail, because at least 1 of the blocks are different, and ans should be false
b1 = Clay(pos=(0, 0, 0))
structure_to_check = [b1, b2, b3, b4, b5, b6, b7, b8, b9]
ans = rrs_assert(structure_to_check, correct_structure, "id", "pos")

# the following assertion should fail, because at least 1 of the blocks are different in position, and ans should be false
b1 = Stone(pos=(1, 0, 0))
structure_to_check = [b1, b2, b3, b4, b5, b6, b7, b8, b9]
ans = rrs_assert(structure_to_check, correct_structure, "id", "pos")

# -----

# end of the specifications for re-redscript
# end of sample_code.py