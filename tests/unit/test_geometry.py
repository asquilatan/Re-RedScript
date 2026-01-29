import pytest
from rrs.stdlib.geometry import rasterize_cylinder

def reference_rasterize_cylinder(base, radius, height, axis='y', fill=False):
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

def test_rasterize_cylinder_correctness():
    test_cases = [
        # (radius, height, axis, fill)
        (5, 10, 'y', False),
        (3, 5, 'x', True),
        (4, 4, 'z', False),
        (1, 1, 'y', True),
        (2, 2, 'y', False),
        (0, 5, 'y', True), # Edge case: r=0 -> single line of points?
        (5, 1, 'y', False) # Edge case: h=1 -> disk
    ]

    base = (10, 10, 10)

    for r, h, axis, fill in test_cases:
        expected = set(reference_rasterize_cylinder(base, r, h, axis, fill))
        actual = set(rasterize_cylinder(base, r, h, axis, fill))

        # Verify equality
        assert actual == expected, f"Failed for r={r}, h={h}, axis={axis}, fill={fill}"
