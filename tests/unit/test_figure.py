import unittest
from rrs.stdlib.figure import Cuboid


class TestCuboid(unittest.TestCase):
    def test_cuboid_filled(self):
        # 3x3x3 filled
        module = Cuboid((0, 0, 0), (2, 2, 2), "stone", fill=True)
        blocks = module.flatten()
        self.assertEqual(len(blocks), 27)
        positions = set([b.pos for b in blocks])
        self.assertEqual(len(positions), 27)

        # Check center point is present
        self.assertIn((1, 1, 1), positions)

    def test_cuboid_hollow(self):
        # 3x3x3 hollow
        # Total 27. Inner 1x1x1 (1 block). Border 26.
        module = Cuboid((0, 0, 0), (2, 2, 2), "stone", fill=False)
        blocks = module.flatten()
        self.assertEqual(len(blocks), 26)
        positions = set([b.pos for b in blocks])
        self.assertEqual(len(positions), 26)

        # Check center point is missing
        self.assertNotIn((1, 1, 1), positions)

        # Check corner is present
        self.assertIn((0, 0, 0), positions)

    def test_cuboid_flat(self):
        # 3x3x1 hollow
        # Total 9. Inner 1x1x(-1) -> empty. All 9 are border?
        # Z range 0..0.
        # Border check: z==z1 or z==z2 (0==0). So all z are border.
        module = Cuboid((0, 0, 0), (2, 2, 0), "stone", fill=False)
        blocks = module.flatten()
        self.assertEqual(len(blocks), 9)

    def test_cuboid_large_hollow(self):
        # 10x10x10 (0..9)
        # 1000 total. Inner 8x8x8 = 512. Border 488.
        module = Cuboid((0, 0, 0), (9, 9, 9), "stone", fill=False)
        blocks = module.flatten()
        self.assertEqual(len(blocks), 1000 - 512)


if __name__ == '__main__':
    unittest.main()
