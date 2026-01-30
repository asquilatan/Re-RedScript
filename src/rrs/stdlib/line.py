from typing import List, Tuple
from rrs.stdlib.geometry import bresenham_line, bezier_curve, catmull_rom_spline, rasterize_sphere
from rrs.stdlib.utils import create_module, place_in_module

def Line(start, end, block, thickness=1):
    m = create_module("Line")
    points = bresenham_line(start, end)

    if thickness <= 1:
        for p in points:
            place_in_module(m, p, block)
    else:
        # Optimization: Pre-calculate sphere offsets and use a set to deduplicate
        # overlapping blocks along the line.
        offsets = rasterize_sphere((0, 0, 0), thickness / 2, fill=True)
        unique_positions = set()

        for p in points:
            px, py, pz = p
            for ox, oy, oz in offsets:
                unique_positions.add((px + ox, py + oy, pz + oz))

        for pos in unique_positions:
            place_in_module(m, pos, block)

    return m

def Path(points: List[Tuple[int, int, int]], block, thickness=1, closed=False, smooth=False):
    m = create_module("Path")
    if len(points) < 2: return m

    path_points = points
    if closed:
        path_points = points + [points[0]]

    if smooth:
        spline_points = catmull_rom_spline(path_points, segments=10)
        for p in spline_points:
                place_in_module(m, p, block)
    else:
        for i in range(len(path_points) - 1):
            seg_points = bresenham_line(path_points[i], path_points[i+1])
            for p in seg_points:
                place_in_module(m, p, block)
    return m

def Bezier(start, c1, c2, end, block, segments=20, thickness=1):
    m = create_module("Bezier")
    points = bezier_curve([start, c1, c2, end], segments)
    for p in points:
            place_in_module(m, p, block)
    return m
