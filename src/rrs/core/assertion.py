from typing import Union, List
from rrs.core.module import Module

def rrs_assert(actual: Union[Module, List[Module]], expected: Union[Module, List[Module]]) -> bool:
    """
    Assert that two modules or structures are identical.
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
        raise AssertionError(f"Block count mismatch: {len(actual_blocks)} != {len(expected_blocks)}")
        
    for b1, b2 in zip(actual_blocks, expected_blocks):
        if b1.pos != b2.pos:
            raise AssertionError(f"Block position mismatch: {b1.pos} != {b2.pos}")
        if b1.id != b2.id:
            raise AssertionError(f"Block ID mismatch: {b1.id} != {b2.id}")
        if b1.properties != b2.properties:
             raise AssertionError(f"Block properties mismatch: {b1.properties} != {b2.properties}")
             
    return True
