import pytest
from rrs.stdlib.geometry import rasterize_sphere


def naive_sphere(center, radius, fill=False):
    cx, cy, cz = center
    points = set()
    r = int(radius)

    for x in range(cx - r, cx + r + 1):
        for y in range(cy - r, cy + r + 1):
            for z in range(cz - r, cz + r + 1):
                dist_sq = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
                if dist_sq <= r**2:
                    if fill:
                        points.add((x, y, z))
                    elif dist_sq >= (r - 1) ** 2:  # Shell
                        points.add((x, y, z))
    return points


@pytest.mark.parametrize(
    "center, radius, fill",
    [
        ((0, 0, 0), 5, False),
        ((0, 0, 0), 5, True),
        ((10, 10, 10), 3, False),
        ((0, 0, 0), 0, False),  # Radius 0
        ((0, 0, 0), 1, False),
        ((0, 0, 0), 10, False),
    ],
)
def test_sphere_rasterization_correctness(center, radius, fill):
    expected = naive_sphere(center, radius, fill)
    actual = set(rasterize_sphere(center, radius, fill))
    assert actual == expected
