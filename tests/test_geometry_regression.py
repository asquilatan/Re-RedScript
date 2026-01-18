
import pytest
from rrs.stdlib.geometry import rasterize_sphere

def naive_sphere(center, radius, fill=False):
    cx, cy, cz = center
    points = set()
    r = int(radius)

    for x in range(cx - r, cx + r + 1):
        for y in range(cy - r, cy + r + 1):
            for z in range(cz - r, cz + r + 1):
                dist_sq = (x - cx)**2 + (y - cy)**2 + (z - cz)**2
                if dist_sq <= r**2:
                    if fill:
                        points.add((x, y, z))
                    elif dist_sq >= (r - 1)**2: # Shell
                        points.add((x, y, z))
    return list(points)

def test_rasterize_sphere_fill():
    # Test small radius
    r = 5
    center = (0, 0, 0)
    expected = set(naive_sphere(center, r, fill=True))
    actual = set(rasterize_sphere(center, r, fill=True))
    assert actual == expected

def test_rasterize_sphere_hollow():
    # Test small radius
    r = 5
    center = (0, 0, 0)
    expected = set(naive_sphere(center, r, fill=False))
    actual = set(rasterize_sphere(center, r, fill=False))
    assert actual == expected

def test_rasterize_sphere_offset():
    # Test offset center
    r = 4
    center = (10, -5, 3)
    expected = set(naive_sphere(center, r, fill=True))
    actual = set(rasterize_sphere(center, r, fill=True))
    assert actual == expected

def test_rasterize_sphere_edge_cases():
    # Radius 0
    assert set(rasterize_sphere((0,0,0), 0, True)) == {(0,0,0)}
    # Existing behavior: Radius 0 hollow is empty
    assert set(rasterize_sphere((0,0,0), 0, False)) == set()

    # Radius 1
    expected_1 = set(naive_sphere((0,0,0), 1, True))
    actual_1 = set(rasterize_sphere((0,0,0), 1, True))
    assert actual_1 == expected_1
