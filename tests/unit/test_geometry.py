import pytest
import math
from rrs.stdlib.geometry import bezier_curve

def test_bezier_curve_ends():
    points = [(0, 0, 0), (50, 50, 50), (100, 0, 0)]
    curve = bezier_curve(points, segments=10)
    assert curve[0] == points[0]
    assert curve[-1] == points[-1]

def test_bezier_curve_linear():
    # A straight line bezier curve
    points = [(0, 0, 0), (10, 10, 10)]
    curve = bezier_curve(points, segments=2)
    # Expected: (0,0,0), (5,5,5), (10,10,10)
    assert (0, 0, 0) in curve
    assert (10, 10, 10) in curve
    # Middle point might vary slightly due to float precision and rounding, but for 2 segments it should be close.
    # actually segments=2 -> t=0, 0.5, 1.0.
    # t=0.5 -> 0.5*P0 + 0.5*P1 = (5,5,5)
    assert (5, 5, 5) in curve

def test_bezier_curve_length():
    points = [(0, 0, 0), (10, 0, 0), (20, 0, 0)]
    segments = 20
    curve = bezier_curve(points, segments=segments)
    # Segments + 1 points
    assert len(curve) == segments + 1
