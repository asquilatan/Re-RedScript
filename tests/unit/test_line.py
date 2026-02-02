
from rrs.stdlib.line import Line


def test_line_simple():
    start = (0, 0, 0)
    end = (10, 0, 0)
    m = Line(start, end, "stone")

    # Bresenham generates 11 points for length 10 inclusive
    assert len(m.children) == 11

    positions = {child.pos for child in m.children}
    expected = {(x, 0, 0) for x in range(11)}
    assert positions == expected


def test_line_thickness():
    start = (0, 0, 0)
    end = (10, 0, 0)
    thickness = 3  # radius 1.5
    m = Line(start, end, "stone", thickness=thickness)

    # Ensure all blocks are within radius distance of the line segment
    # For a horizontal line along x-axis from 0 to 10:
    # Any point (x, y, z) should have sqrt(y^2 + z^2) <= 1.5
    # And -1.5 <= x <= 11.5 approximately (sphere at ends)

    radius = thickness / 2
    max_dist_sq = radius**2

    for child in m.children:
        x, y, z = child.pos
        # Distance to line segment
        # If x is within [0, 10], dist is sqrt(y^2 + z^2)
        # If x < 0, dist is dist((x,y,z), (0,0,0))
        # If x > 10, dist is dist((x,y,z), (10,0,0))

        if 0 <= x <= 10:
            dist_sq = y**2 + z**2
        elif x < 0:
            dist_sq = x**2 + y**2 + z**2
        else:
            dist_sq = (x - 10) ** 2 + y**2 + z**2

        # Allow some tolerance for rasterization
        # Rasterization checks <= radius^2 on integer grid
        # But we are checking mathematically.
        # Actually rasterize_sphere checks dist_sq <= r**2
        # So it should be exact if we use same logic.
        assert dist_sq <= max_dist_sq


def test_line_deduplication():
    start = (0, 0, 0)
    end = (5, 5, 5)
    thickness = 5
    m = Line(start, end, "stone", thickness=thickness)

    # Verify no duplicate positions
    positions = [child.pos for child in m.children]
    assert len(positions) == len(set(positions))
