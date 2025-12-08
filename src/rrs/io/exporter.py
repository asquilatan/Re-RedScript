import litemapy
from rrs.core.module import Module

def rrs_export(module: Module, filepath: str, region_name: str = "Region"):
    """
    Export a Module to a .litematic file.
    """
    blocks = module.flatten()
    
    if not blocks:
        schem = litemapy.Schematic(width=1, height=1, length=1)
        schem.save(filepath)
        return

    min_x = min(b.pos[0] for b in blocks)
    min_y = min(b.pos[1] for b in blocks)
    min_z = min(b.pos[2] for b in blocks)
    
    max_x = max(b.pos[0] for b in blocks)
    max_y = max(b.pos[1] for b in blocks)
    max_z = max(b.pos[2] for b in blocks)
    
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    length = max_z - min_z + 1
    
    # Create Region
    # We use 0,0,0 as the origin of the region within the schematic
    reg = litemapy.Region(0, 0, 0, width, height, length)
    
    # Create Schematic with the region
    schem = litemapy.Schematic(name=module.id, regions={region_name: reg})
    
    for b in blocks:
        x = b.pos[0] - min_x
        y = b.pos[1] - min_y
        z = b.pos[2] - min_z
        
        try:
            # Basic block state creation
            reg[x, y, z] = litemapy.BlockState(b.id)
        except Exception as e:
            print(f"Error setting block {b.id} at {x},{y},{z}: {e}")
            
    schem.save(filepath)
