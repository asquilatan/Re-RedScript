import unittest
from rrs.stdlib.geometry import rasterize_cylinder


class TestCylinder(unittest.TestCase):
    def test_cylinder_hollow_y(self):
        # Radius 2, Height 3
        # Circle at r=2:
        # Points where x^2 + z^2 <= 4 and >= 1
        # (-2,0), (2,0), (0,-2), (0,2), (-1,-1), (-1,1), ...
        # Actually checking count is easier.
        # r=2.
        # (-2, -1): 4+1=5 > 4 (out)
        # (-2, 0): 4 <= 4 (in)
        # (-1, -1): 1+1=2 <= 4 (in). >= 1 (in)
        # (0, 0): 0 < 1 (inner hole)

        # Let's trust the current implementation produces the correct set.
        # I'll just count points for a small example.
        base = (0, 0, 0)
        radius = 5
        height = 10
        points = rasterize_cylinder(base, radius, height, axis="y", fill=False)

        # Verify bounds
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [p[2] for p in points]

        self.assertEqual(min(ys), 0)
        self.assertEqual(max(ys), 9)
        self.assertTrue(min(xs) >= -5)
        self.assertTrue(max(xs) <= 5)
        self.assertTrue(min(zs) >= -5)
        self.assertTrue(max(zs) <= 5)

        # Verify symmetry (roughly)
        self.assertEqual(
            len([p for p in points if p[0] < 0]), len([p for p in points if p[0] > 0])
        )

        # Verify hollow property (no points at center axis except possibly caps)
        # Caps are filled in the current implementation.

        # Check center column
        center_points = [p for p in points if p[0] == 0 and p[2] == 0]
        # Should only be at y=0 and y=9
        self.assertEqual(len(center_points), 2)
        self.assertIn((0, 0, 0), center_points)
        self.assertIn((0, 9, 0), center_points)

    def test_cylinder_filled_y(self):
        base = (0, 0, 0)
        radius = 5
        height = 10
        points = rasterize_cylinder(base, radius, height, axis="y", fill=True)

        # Center column should be full
        center_points = [p for p in points if p[0] == 0 and p[2] == 0]
        self.assertEqual(len(center_points), 10)

    def test_cylinder_axis_x(self):
        base = (0, 0, 0)
        radius = 5
        height = 10
        points = rasterize_cylinder(base, radius, height, axis="x", fill=False)

        xs = [p[0] for p in points]
        self.assertEqual(min(xs), 0)
        self.assertEqual(max(xs), 9)

        # Center line along X should have caps
        center_points = [p for p in points if p[1] == 0 and p[2] == 0]
        self.assertEqual(len(center_points), 2)

    def test_cylinder_axis_z(self):
        base = (0, 0, 0)
        radius = 5
        height = 10
        points = rasterize_cylinder(base, radius, height, axis="z", fill=False)

        zs = [p[2] for p in points]
        self.assertEqual(min(zs), 0)
        self.assertEqual(max(zs), 9)

        # Center line along Z should have caps
        center_points = [p for p in points if p[0] == 0 and p[1] == 0]
        self.assertEqual(len(center_points), 2)

    def test_small_cylinder(self):
        # r=1, h=1
        points = rasterize_cylinder((0, 0, 0), 1, 1, axis="y", fill=False)
        # r=1. r^2=1. (r-1)^2=0.
        # dist_sq <= 1 and dist_sq >= 0.
        # (0,0): d=0. OK.
        # (1,0): d=1. OK.
        # (-1,0): d=1. OK.
        # (0,1): d=1. OK.
        # (0,-1): d=1. OK.
        # y range 0..1 (exclusive?) -> 0.
        # Caps logic: y == by or y == by + h - 1. 0 == 0 or 0 == 0. Both true.
        # So it should generate the full disk.
        # disk points: (0,0), (1,0), (-1,0), (0,1), (0,-1). 5 points.
        self.assertEqual(len(points), 5)


if __name__ == "__main__":
    unittest.main()
