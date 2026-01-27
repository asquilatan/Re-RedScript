
import pytest
from rrs.stdlib.geometry import rasterize_cylinder

def test_cylinder_y_axis_small():
    # Radius 1, Height 2, Y-axis
    # Base at (0,0,0)
    # Circle at y=0:
    #   (0,0,0) - center
    #   (1,0,0), (-1,0,0), (0,0,1), (0,0,-1) - dist_sq=1
    # Circle at y=1:
    #   Same offsets

    # Total points: 5 * 2 = 10

    points = rasterize_cylinder((0,0,0), 1, 2, axis='y', fill=True)
    assert len(points) == 10

    expected = {
        (0,0,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1),
        (0,1,0), (1,1,0), (-1,1,0), (0,1,1), (0,1,-1)
    }
    assert set(points) == expected

def test_cylinder_hollow():
    # Radius 2, Height 3
    # Base (0,0,0)
    # y=0: Full disk (cap)
    # y=1: Ring only (walls)
    # y=2: Full disk (cap)

    # Radius 2:
    # Disk:
    #   (-2..2) x (-2..2)
    #   x^2 + z^2 <= 4
    # Ring:
    #   x^2 + z^2 <= 4 AND x^2 + z^2 >= (2-1)^2 = 1

    points = rasterize_cylinder((0,0,0), 2, 3, axis='y', fill=False)
    points_set = set(points)

    # Check y=0 (Cap)
    # Should include (0,0,0) which is center (dist=0)
    assert (0,0,0) in points_set

    # Check y=1 (Wall)
    # Should NOT include (0,1,0) (dist=0 < 1)
    assert (0,1,0) not in points_set
    # Should include (2,1,0) (dist=4)
    assert (2,1,0) in points_set

    # Check y=2 (Cap)
    assert (0,2,0) in points_set

def test_cylinder_axis_x():
    # Radius 1, Height 2, X-axis
    # Base (0,0,0)
    # Slices at x=0, x=1
    # Circle in (y,z) plane

    points = rasterize_cylinder((0,0,0), 1, 2, axis='x', fill=True)
    expected = {
        (0,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1),
        (1,0,0), (1,1,0), (1,-1,0), (1,0,1), (1,0,-1)
    }
    assert set(points) == expected

def test_cylinder_axis_z():
    # Radius 1, Height 2, Z-axis
    # Base (0,0,0)
    # Slices at z=0, z=1
    # Circle in (x,y) plane

    points = rasterize_cylinder((0,0,0), 1, 2, axis='z', fill=True)
    expected = {
        (0,0,0), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0),
        (0,0,1), (0,1,1), (0,-1,1), (1,0,1), (-1,0,1)
    }
    assert set(points) == expected
