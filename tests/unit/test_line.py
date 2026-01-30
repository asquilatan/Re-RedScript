
import pytest
from rrs.stdlib.line import Line
from rrs.core.block import Block

class MockBlock(Block):
    def __init__(self, pos=(0,0,0), **kwargs):
        super().__init__("minecraft:stone", pos, **kwargs)

def test_line_thin():
    m = Line((0,0,0), (5,0,0), MockBlock(), thickness=1)
    # Bresenham (0,0,0) to (5,0,0) produces 6 points: 0,1,2,3,4,5
    assert len(m.children) == 6
    positions = {b.pos for b in m.children}
    assert (0,0,0) in positions
    assert (5,0,0) in positions

def test_line_thick_coverage():
    # Verify that a thick line covers expected volume
    m = Line((0,0,0), (10,0,0), MockBlock(), thickness=5)

    positions = {b.pos for b in m.children}

    # Radius 2.5 -> int(2).
    # At (0,0,0), we should have (0,2,0) covered.
    assert (0,2,0) in positions
    assert (0,3,0) not in positions # Outside radius 2

    # At (5,0,0), we should have (5,2,0)
    assert (5,2,0) in positions

def test_line_deduplication():
    # After optimization, this should pass.
    # Before optimization, len(children) > len(positions).
    m = Line((0,0,0), (10,0,0), MockBlock(), thickness=5)

    children_count = len(m.children)
    unique_pos_count = len(set(b.pos for b in m.children))

    # We expect strict equality after optimization
    assert children_count == unique_pos_count
