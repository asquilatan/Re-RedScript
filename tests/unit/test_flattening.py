import pytest
from rrs.core.module import Module
from rrs.core.block import Block

def test_flatten_single_block():
    b = Block(id="minecraft:stone", pos=(10, 0, 0))
    flattened = b.flatten()
    assert len(flattened) == 1
    assert flattened[0].pos == (10, 0, 0)
    assert flattened[0].id == "minecraft:stone"

def test_flatten_nested_structure():
    # Parent at (10, 0, 0)
    parent = Module(id="parent", pos=(10, 0, 0))
    
    # Child at (5, 0, 0) relative to parent -> (15, 0, 0) absolute
    child = Module(id="child", pos=(5, 0, 0))
    parent.add(child)
    
    # Block at (1, 0, 0) relative to child -> (16, 0, 0) absolute
    b = Block(id="minecraft:stone", pos=(1, 0, 0))
    child.add(b)
    
    flattened = parent.flatten()
    
    # Flatten should return only Blocks (leaf nodes) with absolute positions
    assert len(flattened) == 1
    assert isinstance(flattened[0], Block)
    assert flattened[0].pos == (16, 0, 0)
