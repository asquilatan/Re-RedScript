from typing import Union, List
from rrs.core.module import Module
from rrs.core.block import Block

def rrs_assert(
    actual: Union[Module, Block, List[Block]], 
    expected: Union[Module, Block, List[Block]], 
    *properties: str,
    ignore_pos: bool = False,
    relative_pos: bool = False
) -> bool:
    """
    Assert that two structures match based on criteria.
    
    Usage:
        assert(structure_1, structure_2, "facing", "id")
    
    Args:
        actual: The structure to test (Module, Block, or list of Blocks)
        expected: The reference structure
        *properties: Property keys to check (e.g. 'facing', 'id'). If none provided, check all.
        ignore_pos: If True, ignore positions entirely (check palette/composition).
        relative_pos: If True, normalize positions to (0,0,0) before comparing.
    """
    # Normalize to list of blocks
    if isinstance(actual, Block):
        actual_blocks = [actual]
    elif isinstance(actual, Module):
        actual_blocks = actual.flatten()
    else:
        actual_blocks = list(actual)
        
    if isinstance(expected, Block):
        expected_blocks = [expected]
    elif isinstance(expected, Module):
        expected_blocks = expected.flatten()
    else:
        expected_blocks = list(expected)
        
    # Relative positioning normalization
    if relative_pos and not ignore_pos:
        if actual_blocks:
            min_x = min(b.pos[0] for b in actual_blocks)
            min_y = min(b.pos[1] for b in actual_blocks)
            min_z = min(b.pos[2] for b in actual_blocks)
            for b in actual_blocks:
                b.pos = (b.pos[0] - min_x, b.pos[1] - min_y, b.pos[2] - min_z)
                
        if expected_blocks:
            min_x = min(b.pos[0] for b in expected_blocks)
            min_y = min(b.pos[1] for b in expected_blocks)
            min_z = min(b.pos[2] for b in expected_blocks)
            for b in expected_blocks:
                b.pos = (b.pos[0] - min_x, b.pos[1] - min_y, b.pos[2] - min_z)

    # Sort to align for comparison
    if not ignore_pos:
        actual_blocks.sort(key=lambda b: b.pos)
        expected_blocks.sort(key=lambda b: b.pos)
    else:
        # If ignoring position, sort by ID so we can match composition
        actual_blocks.sort(key=lambda b: (b.id, str(b.properties)))
        expected_blocks.sort(key=lambda b: (b.id, str(b.properties)))
    
    if len(actual_blocks) != len(expected_blocks):
        raise AssertionError(f"Block count mismatch: {len(actual_blocks)} != {len(expected_blocks)}")
        
    # Convert properties tuple to list for checking
    props_to_check = list(properties) if properties else None
    
    for i, (b1, b2) in enumerate(zip(actual_blocks, expected_blocks)):
        if not ignore_pos:
            if b1.pos != b2.pos:
                raise AssertionError(f"Block #{i} position mismatch: {b1.pos} != {b2.pos}")
        
        # Always check ID if "id" is in properties or if no properties specified
        check_id = props_to_check is None or "id" in props_to_check
        if check_id and b1.id != b2.id:
            raise AssertionError(f"Block #{i} ID mismatch: {b1.id} != {b2.id}")
            
        if props_to_check is None:
            # Check all properties
            if b1.properties != b2.properties:
                 raise AssertionError(f"Block #{i} ({b1.id}) properties mismatch: {b1.properties} != {b2.properties}")
        else:
            # Check only specified properties (excluding "id" which is handled above)
            for prop in props_to_check:
                if prop == "id":
                    continue  # Already checked above
                val1 = b1.properties.get(prop)
                val2 = b2.properties.get(prop)
                if val1 != val2:
                    raise AssertionError(f"Block #{i} ({b1.id}) property '{prop}' mismatch: {val1} != {val2}")
             
    return True
