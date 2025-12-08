import pytest
from rrs.core.module import Module
from rrs.core.block import Stone, Piston
from rrs.core.assertion import rrs_assert

def test_assert_matching_single_block():
    b1 = Stone(pos=(0, 0, 0))
    b2 = Stone(pos=(0, 0, 0))
    assert rrs_assert(b1, b2) is True

def test_assert_mismatch_id():
    b1 = Stone(pos=(0, 0, 0))
    b2 = Piston(pos=(0, 0, 0))
    with pytest.raises(AssertionError, match="Block ID mismatch"):
        rrs_assert(b1, b2)

def test_assert_mismatch_pos():
    b1 = Stone(pos=(0, 0, 0))
    b2 = Stone(pos=(0, 1, 0))
    with pytest.raises(AssertionError, match="Block position mismatch"):
        rrs_assert(b1, b2)

def test_assert_structure():
    m1 = Module("M1")
    m1.add(Stone(pos=(0, 0, 0)))
    m1.add(Stone(pos=(0, 1, 0)))
    
    m2 = Module("M2")
    m2.add(Stone(pos=(0, 0, 0)))
    m2.add(Stone(pos=(0, 1, 0)))
    
    assert rrs_assert(m1, m2) is True

def test_assert_structure_mismatch_count():
    m1 = Module("M1")
    m1.add(Stone(pos=(0, 0, 0)))
    
    m2 = Module("M2")
    m2.add(Stone(pos=(0, 0, 0)))
    m2.add(Stone(pos=(0, 1, 0)))
    
    with pytest.raises(AssertionError, match="Block count mismatch"):
        rrs_assert(m1, m2)
