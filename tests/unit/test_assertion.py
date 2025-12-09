import pytest
from rrs.core.module import Module
from rrs.core.block import Block
from rrs.core.assertion import rrs_assert

def test_assert_matching_single_block():
    b1 = Block("minecraft:stone", pos=(0, 0, 0))
    b2 = Block("minecraft:stone", pos=(0, 0, 0))
    assert rrs_assert(b1, b2) is True

def test_assert_mismatch_id():
    b1 = Block("minecraft:stone", pos=(0, 0, 0))
    b2 = Block("minecraft:piston", pos=(0, 0, 0))
    with pytest.raises(AssertionError, match="ID mismatch"):
        rrs_assert(b1, b2)

def test_assert_mismatch_pos():
    b1 = Block("minecraft:stone", pos=(0, 0, 0))
    b2 = Block("minecraft:stone", pos=(0, 1, 0))
    with pytest.raises(AssertionError, match="position mismatch"):
        rrs_assert(b1, b2)

def test_assert_structure():
    m1 = Module("M1")
    m1.add(Block("minecraft:stone", pos=(0, 0, 0)))
    m1.add(Block("minecraft:stone", pos=(0, 1, 0)))
    
    m2 = Module("M2")
    m2.add(Block("minecraft:stone", pos=(0, 0, 0)))
    m2.add(Block("minecraft:stone", pos=(0, 1, 0)))
    
    assert rrs_assert(m1, m2) is True

def test_assert_structure_mismatch_count():
    m1 = Module("M1")
    m1.add(Block("minecraft:stone", pos=(0, 0, 0)))
    
    m2 = Module("M2")
    m2.add(Block("minecraft:stone", pos=(0, 0, 0)))
    m2.add(Block("minecraft:stone", pos=(0, 1, 0)))
    
    with pytest.raises(AssertionError, match="Block count mismatch"):
        rrs_assert(m1, m2)
