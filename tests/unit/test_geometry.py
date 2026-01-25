
import pytest
from rrs.stdlib.geometry import rasterize_sphere

def test_rasterize_sphere_fill_false_r1():
    # R=1. Shell condition: dist_sq >= 0. So same as fill=True.
    center = (0, 0, 0)
    radius = 1
    points = rasterize_sphere(center, radius, fill=False)
    # Points with d^2 <= 1:
    # (0,0,0) d=0
    # (±1,0,0) d=1
    # (0,±1,0) d=1
    # (0,0,±1) d=1
    # Total 1 + 6 = 7 points.
    assert len(points) == 7
    assert (0, 0, 0) in points
    assert (1, 0, 0) in points

def test_rasterize_sphere_fill_false_r2():
    # R=2. Shell condition: dist_sq >= 1. d^2 <= 4.
    # Excludes (0,0,0).
    center = (0, 0, 0)
    radius = 2
    points = rasterize_sphere(center, radius, fill=False)

    assert (0, 0, 0) not in points
    assert (2, 0, 0) in points # d^2=4
    assert (1, 0, 0) in points # d^2=1

    # Check bounds
    for p in points:
        d2 = p[0]**2 + p[1]**2 + p[2]**2
        assert 1 <= d2 <= 4

def test_rasterize_sphere_fill_true_r2():
    center = (0, 0, 0)
    radius = 2
    points = rasterize_sphere(center, radius, fill=True)

    # Should include (0,0,0)
    assert (0, 0, 0) in points

    # Check bounds
    for p in points:
        d2 = p[0]**2 + p[1]**2 + p[2]**2
        assert d2 <= 4

def test_rasterize_sphere_offset():
    center = (10, 10, 10)
    radius = 2
    points = rasterize_sphere(center, radius, fill=True)

    for p in points:
        # Check relative distance
        d2 = (p[0]-10)**2 + (p[1]-10)**2 + (p[2]-10)**2
        assert d2 <= 4
