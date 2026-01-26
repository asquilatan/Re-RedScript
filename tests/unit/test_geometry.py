import pytest
from rrs.stdlib.geometry import rasterize_cylinder

def test_rasterize_cylinder_simple():
    # Radius 1, Height 1, should be small
    # Base at 0,0,0
    points = rasterize_cylinder((0,0,0), radius=1, height=1, axis='y', fill=True)
    # R=1. points: (0,0), (1,0), (-1,0), (0,1), (0,-1) relative to center in XZ.
    # Total 5 points.
    assert len(points) == 5
    expected = {(0,0,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)}
    assert set(points) == expected

def test_rasterize_cylinder_axis():
    # Height 5, y-axis
    points_y = rasterize_cylinder((0,0,0), radius=1, height=5, axis='y', fill=True)
    ys = [p[1] for p in points_y]
    assert min(ys) == 0
    assert max(ys) == 4
    assert len(points_y) == 5 * 5 # 5 points per slice * 5 slices

    # x-axis
    points_x = rasterize_cylinder((0,0,0), radius=1, height=5, axis='x', fill=True)
    xs = [p[0] for p in points_x]
    assert min(xs) == 0
    assert max(xs) == 4
    assert len(points_x) == 5 * 5

    # z-axis
    points_z = rasterize_cylinder((0,0,0), radius=1, height=5, axis='z', fill=True)
    zs = [p[2] for p in points_z]
    assert min(zs) == 0
    assert max(zs) == 4
    assert len(points_z) == 5 * 5

def test_rasterize_cylinder_fill_false():
    # R=2. (0,0) center.
    # Points with dist_sq <= 4.
    # Points with dist_sq >= (2-1)^2 = 1.
    # So dist_sq in [1, 4].
    # (0,0) has dist_sq=0. Should be excluded unless cap.

    height = 3
    points = rasterize_cylinder((0,0,0), radius=2, height=height, axis='y', fill=False)
    point_set = set(points)

    # Bottom cap (y=0) should have (0,0,0)
    assert (0, 0, 0) in point_set

    # Top cap (y=2) should have (0,0,2) -> wait, (0,2,0)
    assert (0, 2, 0) in point_set

    # Middle (y=1) should NOT have (0,1,0)
    assert (0, 1, 0) not in point_set

    # Middle (y=1) should have (2,1,0) because dist_sq=4 >= 1
    assert (2, 1, 0) in point_set

def test_rasterize_cylinder_radius_zero():
    # R=0. Only center point (0,0) matches dist_sq <= 0.
    # dist_sq >= (0-1)^2 = 1. 0 >= 1 False.
    # So only caps are drawn if fill=False.

    # Fill=True
    points = rasterize_cylinder((0,0,0), radius=0, height=3, axis='y', fill=True)
    assert len(points) == 3 # (0,0,0), (0,1,0), (0,2,0)

    # Fill=False
    points_hollow = rasterize_cylinder((0,0,0), radius=0, height=3, axis='y', fill=False)
    # only caps: y=0 and y=2.
    assert len(points_hollow) == 2
    assert (0,0,0) in points_hollow
    assert (0,2,0) in points_hollow
    assert (0,1,0) not in points_hollow
