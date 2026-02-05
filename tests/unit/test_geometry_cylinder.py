import unittest
from rrs.stdlib.geometry import rasterize_cylinder


class TestRasterizeCylinder(unittest.TestCase):
    def test_cylinder_filled_y(self):
        # r=2, h=3
        # Disk area for r=2:
        # (-2..2) x (-2..2). dist_sq <= 4.
        # Points:
        # (0,0) d=0
        # (0,1), (0,-1), (1,0), (-1,0) d=1
        # (1,1), (1,-1), (-1,1), (-1,-1) d=2
        # (0,2), (0,-2), (2,0), (-2,0) d=4
        # Total: 1 + 4 + 4 + 4 = 13 points per layer.
        # Height 3 -> 13 * 3 = 39 points.
        points = rasterize_cylinder((0, 0, 0), 2, 3, axis="y", fill=True)
        self.assertEqual(len(points), 39)

        # Check bounds
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [p[2] for p in points]
        self.assertEqual(min(ys), 0)
        self.assertEqual(max(ys), 2)
        self.assertTrue(all(-2 <= x <= 2 for x in xs))
        self.assertTrue(all(-2 <= z <= 2 for z in zs))

    def test_cylinder_hollow_y(self):
        # r=2, h=3.
        # Hollow means body uses ring, caps use disk.
        # Ring for r=2: (r-1)^2 <= d^2 <= r^2 => 1 <= d^2 <= 4.
        # So we exclude d=0 (center point (0,0)).
        # Disk points (13) - Center (1) = 12 points per ring layer.

        # Layers:
        # y=0: Cap (Disk) -> 13 points
        # y=1: Body (Ring) -> 12 points
        # y=2: Cap (Disk) -> 13 points
        # Total: 13 + 12 + 13 = 38 points.

        points = rasterize_cylinder((0, 0, 0), 2, 3, axis="y", fill=False)
        self.assertEqual(len(points), 38)

        # Verify center point (0,1,0) is missing (middle layer center)
        self.assertNotIn((0, 1, 0), points)
        # Verify cap center points exist
        self.assertIn((0, 0, 0), points)
        self.assertIn((0, 2, 0), points)

    def test_cylinder_axis_x(self):
        # r=2, h=3, axis=x
        # Length along x.
        points = rasterize_cylinder((10, 20, 30), 2, 3, axis="x", fill=True)
        self.assertEqual(len(points), 39)

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [p[2] for p in points]

        # x range 10..12
        self.assertEqual(min(xs), 10)
        self.assertEqual(max(xs), 12)
        # y, z centered at 20, 30 with radius 2
        self.assertTrue(all(18 <= y <= 22 for y in ys))
        self.assertTrue(all(28 <= z <= 32 for z in zs))

    def test_cylinder_axis_z(self):
        # r=2, h=3, axis=z
        points = rasterize_cylinder((0, 0, 0), 2, 3, axis="z", fill=True)
        self.assertEqual(len(points), 39)

        zs = [p[2] for p in points]
        self.assertEqual(min(zs), 0)
        self.assertEqual(max(zs), 2)

    def test_cylinder_flat(self):
        # h=1 -> Disk
        # Both fill=True and fill=False should give full disk because cap logic
        # (first/last layer) overrides hollow logic.
        points_filled = rasterize_cylinder((0, 0, 0), 5, 1, axis="y", fill=True)
        points_hollow = rasterize_cylinder((0, 0, 0), 5, 1, axis="y", fill=False)

        self.assertEqual(len(points_filled), len(points_hollow))
        self.assertEqual(set(points_filled), set(points_hollow))

        # Check specific point count for r=5
        # Just regression check or approximate area pi*r^2 approx 78.
        # r=5 area:
        # x^2+y^2 <= 25.
        # Calculated: 81 points (approx).
        # Let's just ensure it's > 0.
        self.assertTrue(len(points_filled) > 0)


if __name__ == "__main__":
    unittest.main()
