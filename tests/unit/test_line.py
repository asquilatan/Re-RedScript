
import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

from rrs.stdlib.line import Line
from rrs.core.module import Module
from rrs.core.block import Block

def test_line_thickness_1():
    start = (0, 0, 0)
    end = (10, 0, 0)
    m = Line(start, end, "stone", thickness=1)

    # Length 11 points (0 to 10 inclusive)
    assert len(m.children) == 11

    positions = set(c.pos for c in m.children)
    assert len(positions) == 11
    assert (0,0,0) in positions
    assert (10,0,0) in positions

def test_line_thickness_3_deduplication():
    start = (0, 0, 0)
    end = (5, 0, 0)
    m = Line(start, end, "stone", thickness=3)

    children_count = len(m.children)
    positions = set(c.pos for c in m.children)

    # Assert no duplicates
    assert children_count == len(positions)

    # Assert it's thicker than 1 line
    assert len(positions) > 6

    # Check bounds (thickness 3 means radius 1.5 -> int radius 1)
    # So y and z should range from -1 to 1
    ys = [p[1] for p in positions]
    zs = [p[2] for p in positions]
    assert min(ys) >= -1
    assert max(ys) <= 1
    assert min(zs) >= -1
    assert max(zs) <= 1

def test_line_correctness_diagonal():
    start = (0, 0, 0)
    end = (10, 10, 10)
    m = Line(start, end, "stone", thickness=3)

    children_count = len(m.children)
    positions = set(c.pos for c in m.children)

    assert children_count == len(positions)
    assert (0,0,0) in positions
    assert (10,10,10) in positions
