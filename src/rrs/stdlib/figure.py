from rrs.stdlib.geometry import rasterize_sphere, rasterize_cylinder
from rrs.stdlib.utils import create_module, place_in_module

def Sphere(center, radius, block, fill=False):
    m = create_module("Sphere")
    points = rasterize_sphere(center, radius, fill)
    for p in points:
        place_in_module(m, p, block)
    return m

def Cuboid(pos1, pos2, block, fill=False):
    m = create_module("Cuboid")
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2

    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    z_min, z_max = min(z1, z2), max(z1, z2)

    # Helper to iterate over range including stop
    def safe_range(start, stop):
        return range(start, stop + 1)

    if fill:
        for x in safe_range(x_min, x_max):
            for y in safe_range(y_min, y_max):
                for z in safe_range(z_min, z_max):
                    place_in_module(m, (x, y, z), block)
        return m

    # Optimized hollow cuboid generation (fill=False)
    # Iterate over faces to avoid checking "is_border" for every point in volume

    # 1. X faces (Left and Right)
    # Covers full Y and Z ranges
    xs = {x_min, x_max}
    for x in xs:
        for y in safe_range(y_min, y_max):
            for z in safe_range(z_min, z_max):
                place_in_module(m, (x, y, z), block)

    # 2. Y faces (Top and Bottom)
    # Exclude X edges (already covered by X faces)
    # Range is strictly between x_min and x_max
    ys = {y_min, y_max}
    inner_xs = range(x_min + 1, x_max)
    if inner_xs: # Optimization: skip if range is empty
        for y in ys:
            for x in inner_xs:
                for z in safe_range(z_min, z_max):
                    place_in_module(m, (x, y, z), block)

    # 3. Z faces (Front and Back)
    # Exclude X edges (covered by X faces) AND Y edges (covered by Y faces)
    zs = {z_min, z_max}
    inner_ys = range(y_min + 1, y_max)
    if inner_xs and inner_ys: # Optimization: skip if either range is empty
         for z in zs:
            for x in inner_xs:
                for y in inner_ys:
                    place_in_module(m, (x, y, z), block)

    return m

def Cylinder(base, radius, height, block, axis='y', fill=False):
    m = create_module("Cylinder")
    points = rasterize_cylinder(base, radius, height, axis, fill)
    for p in points:
        place_in_module(m, p, block)
    return m
