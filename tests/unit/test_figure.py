import pytest
from rrs.stdlib.figure import Cuboid
from rrs.core.block import Block

class MockBlock(Block):
    def __init__(self, name="stone", pos=(0,0,0), **kwargs):
        super().__init__(name, pos, **kwargs)

def test_cuboid_filled():
    # 2x2x2 filled cuboid
    m = Cuboid((0, 0, 0), (1, 1, 1), MockBlock("stone"), fill=True)
    blocks = m.flatten()
    assert len(blocks) == 8

    positions = {b.pos for b in blocks}
    expected_positions = {
        (0,0,0), (0,0,1), (0,1,0), (0,1,1),
        (1,0,0), (1,0,1), (1,1,0), (1,1,1)
    }
    assert positions == expected_positions

def test_cuboid_hollow_small():
    # 2x2x2 hollow cuboid (same as filled because all are surface)
    m = Cuboid((0, 0, 0), (1, 1, 1), MockBlock("stone"), fill=False)
    blocks = m.flatten()
    assert len(blocks) == 8

def test_cuboid_hollow_3x3x3():
    # 3x3x3 hollow cuboid
    # Total volume 27. Center (1,1,1) should be empty.
    # Surface blocks = 27 - 1 = 26.
    m = Cuboid((0, 0, 0), (2, 2, 2), MockBlock("stone"), fill=False)
    blocks = m.flatten()
    assert len(blocks) == 26

    positions = {b.pos for b in blocks}
    assert (1,1,1) not in positions
    assert (0,0,0) in positions
    assert (2,2,2) in positions

def test_cuboid_flat_hollow():
    # 10x10x1 flat cuboid (plate)
    # Should be all filled essentially as it has no "internal" volume in Z
    m = Cuboid((0, 0, 0), (9, 9, 0), MockBlock("stone"), fill=False)
    blocks = m.flatten()
    # 10 * 10 = 100 blocks
    assert len(blocks) == 100

def test_cuboid_line_hollow():
    # 10x1x1 line
    m = Cuboid((0, 0, 0), (9, 0, 0), MockBlock("stone"), fill=False)
    blocks = m.flatten()
    assert len(blocks) == 10
