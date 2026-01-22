import unittest
import random
from rrs.stdlib.figure import Cuboid
from rrs.core.block import Block


def extract_points(module):
    points = set()
    for child in module.children:
        if isinstance(child, Block):
            points.add(child.pos)
    return points


def _reference_cuboid(pos1, pos2, fill=False):
    points = set()
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2

    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    z_min, z_max = min(z1, z2), max(z1, z2)

    xs = range(x_min, x_max + 1)
    ys = range(y_min, y_max + 1)
    zs = range(z_min, z_max + 1)

    for x in xs:
        for y in ys:
            for z in zs:
                is_border = (
                    x == x_min or x == x_max or
                    y == y_min or y == y_max or
                    z == z_min or z == z_max
                )
                if fill or is_border:
                    points.add((x, y, z))
    return points


class TestFigure(unittest.TestCase):
    def test_cuboid_hollow_random(self):
        """Test optimized Cuboid vs reference for hollow cuboids."""
        for _ in range(20):
            p1 = (random.randint(-10, 10),
                  random.randint(-10, 10),
                  random.randint(-10, 10))
            p2 = (random.randint(-10, 10),
                  random.randint(-10, 10),
                  random.randint(-10, 10))

            expected = _reference_cuboid(p1, p2, fill=False)

            mod = Cuboid(p1, p2, "stone", fill=False)
            actual = extract_points(mod)

            msg = f"Size mismatch for p1={p1}, p2={p2} (hollow)"
            self.assertEqual(len(actual), len(expected), msg)
            msg = f"Content mismatch for p1={p1}, p2={p2} (hollow)"
            self.assertEqual(actual, expected, msg)

    def test_cuboid_fill_random(self):
        """Test Cuboid vs reference for filled cuboids."""
        for _ in range(5):
            p1 = (random.randint(-5, 5),
                  random.randint(-5, 5),
                  random.randint(-5, 5))
            p2 = (random.randint(-5, 5),
                  random.randint(-5, 5),
                  random.randint(-5, 5))

            expected = _reference_cuboid(p1, p2, fill=True)
            mod = Cuboid(p1, p2, "stone", fill=True)
            actual = extract_points(mod)

            msg = f"Size mismatch for p1={p1}, p2={p2} (fill)"
            self.assertEqual(len(actual), len(expected), msg)
            msg = f"Content mismatch for p1={p1}, p2={p2} (fill)"
            self.assertEqual(actual, expected, msg)

    def test_cuboid_edge_cases(self):
        """Test 1x1x1, 2x2x2, lines, planes."""
        cases = [
            ((0, 0, 0), (0, 0, 0)),  # Point
            ((0, 0, 0), (1, 0, 0)),  # Line
            ((0, 0, 0), (1, 1, 0)),  # Plane
            ((0, 0, 0), (1, 1, 1)),  # Small cube
        ]
        for p1, p2 in cases:
            for fill in [True, False]:
                expected = _reference_cuboid(p1, p2, fill=fill)
                mod = Cuboid(p1, p2, "stone", fill=fill)
                actual = extract_points(mod)
                msg = f"Mismatch for case p1={p1}, p2={p2}, fill={fill}"
                self.assertEqual(actual, expected, msg)
