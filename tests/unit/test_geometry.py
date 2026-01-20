import math
import pytest
from rrs.stdlib.geometry import rasterize_cylinder

def naive_rasterize_cylinder(base, radius, height, axis='y', fill=False):
    bx, by, bz = base
    points = set()
    r = int(radius)
    h = int(height)

    # Simple axis alignment
    if axis == 'y':
        for y in range(by, by + h):
            for x in range(bx - r, bx + r + 1):
                for z in range(bz - r, bz + r + 1):
                    dist_sq = (x - bx)**2 + (z - bz)**2
                    if dist_sq <= r**2:
                        if fill or dist_sq >= (r-1)**2 or y == by or y == by + h - 1:
                             points.add((x, y, z))
    elif axis == 'x':
         for x in range(bx, bx + h):
            for y in range(by - r, by + r + 1):
                for z in range(bz - r, bz + r + 1):
                    dist_sq = (y - by)**2 + (z - bz)**2
                    if dist_sq <= r**2:
                        if fill or dist_sq >= (r-1)**2 or x == bx or x == bx + h - 1:
                             points.add((x, y, z))
    elif axis == 'z':
        for z in range(bz, bz + h):
            for x in range(bx - r, bx + r + 1):
                for y in range(by - r, by + r + 1):
                    dist_sq = (x - bx)**2 + (y - by)**2
                    if dist_sq <= r**2:
                        if fill or dist_sq >= (r-1)**2 or z == bz or z == bz + h - 1:
                             points.add((x, y, z))

    return list(points)

@pytest.mark.parametrize("radius, height, axis, fill", [
    (5, 10, 'y', False),
    (5, 10, 'y', True),
    (5, 10, 'x', False),
    (5, 10, 'z', False),
    (2, 5, 'y', False),
    (10, 5, 'y', False),
    (1, 5, 'y', False),
    (0, 5, 'y', False),
])
def test_rasterize_cylinder_correctness(radius, height, axis, fill):
    base = (0, 0, 0)
    expected = set(naive_rasterize_cylinder(base, radius, height, axis, fill))
    actual = set(rasterize_cylinder(base, radius, height, axis, fill))
    assert actual == expected
