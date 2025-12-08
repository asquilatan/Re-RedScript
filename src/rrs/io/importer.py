import litemapy
from rrs.core.module import Module
from rrs.core.block import Block

def rrs_import(filepath: str, module_name: str) -> Module:
    """
    Import a .litematic file as a Module.
    """
    schem = litemapy.Schematic.load(filepath)
    
    root = Module(id=module_name)
    
    for reg_name, reg in schem.regions.items():
        # Iterate over all blocks in the region
        for x, y, z in reg.allblockpos():
            block = reg[x, y, z]
            if block.id == "minecraft:air":
                continue
                
            b = Block(id=block.id, pos=(x, y, z))
            root.add(b)
            
    return root
