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

    if fill:
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    place_in_module(m, (x, y, z), block)
    else:
        # 1. Z faces (Top/Bottom) - Full XY planes
        for z in {z_min, z_max}:
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    place_in_module(m, (x, y, z), block)

        # 2. Y faces (Front/Back) - Exclude Z faces (top/bottom edges)
        for y in {y_min, y_max}:
            for z in range(z_min + 1, z_max):
                for x in range(x_min, x_max + 1):
                    place_in_module(m, (x, y, z), block)

        # 3. X faces (Left/Right) - Exclude Z and Y faces (edges)
        for x in {x_min, x_max}:
            for z in range(z_min + 1, z_max):
                for y in range(y_min + 1, y_max):
                    place_in_module(m, (x, y, z), block)
    return m


def Cylinder(base, radius, height, block, axis='y', fill=False):
    m = create_module("Cylinder")
    points = rasterize_cylinder(base, radius, height, axis, fill)
    for p in points:
        place_in_module(m, p, block)
    return m
