from typing import Union, List
from rrs.core.module import Module

def rrs_assert(
    actual: Union[Module, List[Module]], 
    expected: Union[Module, List[Module]], 
    properties: List[str] = None,
    ignore_pos: bool = False,
    relative_pos: bool = False
) -> bool:
    """
    Assert that two modules matches based on criteria.
    
    Args:
        actual: The module to test
        expected: The reference module
        properties: List of property keys to check (e.g. ['facing']). If None, check all.
        ignore_pos: If True, ignore positions entirely (check palette/composition).
        relative_pos: If True, normalize positions to (0,0,0) before comparing.
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
        
    for i, (b1, b2) in enumerate(zip(actual_blocks, expected_blocks)):
        if not ignore_pos:
            if b1.pos != b2.pos:
                raise AssertionError(f"Block #{i} position mismatch: {b1.pos} != {b2.pos}")
        
        if b1.id != b2.id:
            raise AssertionError(f"Block #{i} ID mismatch: {b1.id} != {b2.id}")
            
        if properties is None:
            # key-value pairs must match exactly
            if b1.properties != b2.properties:
                 raise AssertionError(f"Block #{i} ({b1.id}) properties mismatch: {b1.properties} != {b2.properties}")
        else:
            # Check specific properties
            for prop in properties:
                val1 = b1.properties.get(prop)
                val2 = b2.properties.get(prop)
                if val1 != val2:
                    raise AssertionError(f"Block #{i} ({b1.id}) property '{prop}' mismatch: {val1} != {val2}")
             
    return True
