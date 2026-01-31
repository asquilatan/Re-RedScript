import pytest
from rrs.stdlib.geometry import rasterize_cylinder

def get_circle_points(radius):
    points = []
    r = int(radius)
    r_sq = r * r
    for u in range(-r, r + 1):
        for v in range(-r, r + 1):
            if u*u + v*v <= r_sq:
                points.append((u, v))
    return points

def get_ring_points(radius):
    points = []
    r = int(radius)
    r_sq = r * r
    inner_r_sq = (r - 1) ** 2
    for u in range(-r, r + 1):
        for v in range(-r, r + 1):
            d2 = u*u + v*v
            if d2 <= r_sq and d2 >= inner_r_sq:
                points.append((u, v))
    return points

@pytest.mark.parametrize("axis", ['x', 'y', 'z'])
@pytest.mark.parametrize("fill", [True, False])
def test_rasterize_cylinder_properties(axis, fill):
    base = (10, 20, 30)
    bx, by, bz = base
    radius = 5
    height = 10

    points = rasterize_cylinder(base, radius, height, axis, fill)

    # Check boundaries and geometry
    disk_pts = get_circle_points(radius)
    ring_pts = get_ring_points(radius)

    disk_area = len(disk_pts)
    ring_area = len(ring_pts)

    # Calculate expected number of points
    if fill:
        expected_count = disk_area * height
    else:
        # Caps are full disks, middle are rings
        # Top + Bottom = 2 * disk_area
        # Middle = (height - 2) * ring_area
        expected_count = 2 * disk_area + (height - 2) * ring_area

    assert len(points) == expected_count

    # Check each point validity
    for p in points:
        px, py, pz = p

        if axis == 'y':
            # Height check
            assert by <= py < by + height
            # Circle check
            dist_sq = (px - bx)**2 + (pz - bz)**2
            assert dist_sq <= radius**2

            if not fill:
                # If not cap, must be ring
                is_cap = (py == by) or (py == by + height - 1)
                if not is_cap:
                    assert dist_sq >= (radius - 1)**2

        elif axis == 'x':
            assert bx <= px < bx + height
            dist_sq = (py - by)**2 + (pz - bz)**2
            assert dist_sq <= radius**2

            if not fill:
                is_cap = (px == bx) or (px == bx + height - 1)
                if not is_cap:
                    assert dist_sq >= (radius - 1)**2

        elif axis == 'z':
            assert bz <= pz < bz + height
            dist_sq = (px - bx)**2 + (py - by)**2
            assert dist_sq <= radius**2

            if not fill:
                is_cap = (pz == bz) or (pz == bz + height - 1)
                if not is_cap:
                    assert dist_sq >= (radius - 1)**2
