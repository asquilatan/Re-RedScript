
import pytest
from rrs.stdlib.geometry import rasterize_sphere

# Reference implementation for correctness checking
def reference_rasterize_sphere(center, radius, fill=False):
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
    return sorted(list(points))

class TestGeometrySphere:
    @pytest.mark.parametrize("radius", [1, 2, 5, 10, 20])
    @pytest.mark.parametrize("center", [(0,0,0), (10, 20, 30)])
    @pytest.mark.parametrize("fill", [True, False])
    def test_rasterize_sphere_correctness(self, center, radius, fill):
        """Verify that the optimized implementation matches the brute-force reference."""
        ref = reference_rasterize_sphere(center, radius, fill)
        opt = sorted(rasterize_sphere(center, radius, fill))

        assert len(opt) == len(ref), f"Count mismatch for r={radius}, fill={fill}"
        assert opt == ref, f"Content mismatch for r={radius}, fill={fill}"

    def test_sphere_determinism(self):
        """Verify that the output is deterministic (same order across calls)."""
        # Note: The new implementation uses list append, so it should be deterministic by definition.
        # This test ensures we don't accidentally revert to non-deterministic set behavior.
        p1 = rasterize_sphere((0,0,0), 10, False)
        p2 = rasterize_sphere((0,0,0), 10, False)
        assert p1 == p2
