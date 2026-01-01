
import pytest
from rrs.stdlib.geometry import rasterize_sphere

def test_rasterize_sphere_simple():
    center = (0, 0, 0)
    radius = 2
    # Sphere r=2.
    # Points where x^2+y^2+z^2 <= 4
    # (0,0,0) d=0
    # (1,0,0) d=1
    # (2,0,0) d=4 -> included
    # (1,1,1) d=3
    # (1,1,2) d=6 -> excluded

    # Original implementation logic: dist_sq <= r**2
    points = rasterize_sphere(center, radius, fill=True)
    points_set = set(points)

    # Check specific points
    assert (0, 0, 0) in points_set
    assert (2, 0, 0) in points_set
    assert (0, 2, 0) in points_set
    assert (0, 0, 2) in points_set

    # (2, 1, 0) -> 4+1=5 > 4. Excluded.
    assert (2, 1, 0) not in points_set

    # Size check is harder to be exact without calculating, but we can trust the logic if boundaries are correct.

    # Shell check
    # r=2. Shell: dist_sq >= (2-1)^2 = 1.
    # So dist_sq in [1, 4].
    # (0,0,0) is dist_sq=0 -> Excluded.
    points_shell = rasterize_sphere(center, radius, fill=False)
    shell_set = set(points_shell)

    assert (0, 0, 0) not in shell_set
    assert (2, 0, 0) in shell_set # d=4
    assert (1, 0, 0) in shell_set # d=1

def test_rasterize_sphere_offset():
    center = (10, 10, 10)
    radius = 1
    # r=1. dist_sq <= 1.
    # Center (10,10,10) d=0.
    # Neighbors (11,10,10) d=1.
    # (11,11,10) d=2 > 1. Excluded.

    points = rasterize_sphere(center, radius, fill=True)
    expected_count = 1 + 6 # Center + 6 faces
    assert len(points) == expected_count
    for p in points:
        # Check simple Manhattan distance for rough bounds?
        # Actually just check they are within radius.
        d2 = (p[0]-10)**2 + (p[1]-10)**2 + (p[2]-10)**2
        assert d2 <= 1

    # Shell
    # r=1. dist_sq >= 0.
    # So all points included?
    # Logic: dist_sq >= (r-1)**2 = 0.
    # Yes, all points.
    points_shell = rasterize_sphere(center, radius, fill=False)
    assert len(points_shell) == len(points)
    assert set(points_shell) == set(points)

def test_rasterize_sphere_large():
    # Just a smoke test for larger sphere
    points = rasterize_sphere((0,0,0), 10, fill=True)
    assert len(points) > 0
    # Approx volume 4/3 pi r^3 = 4/3 * 3.14 * 1000 = 4188
    # Should be roughly that.
    assert 3000 < len(points) < 5000
