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

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    min_z, max_z = min(z1, z2), max(z1, z2)

    if fill:
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    place_in_module(m, (x, y, z), block)
    else:
        # Optimize for hollow cuboid: only iterate faces
        # 1. Z faces (Top/Bottom)
        for z in {min_z, max_z}:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    place_in_module(m, (x, y, z), block)

        # 2. Y faces (Front/Back) - excluding Z faces
        for y in {min_y, max_y}:
            for x in range(min_x, max_x + 1):
                for z in range(min_z + 1, max_z):
                    place_in_module(m, (x, y, z), block)

        # 3. X faces (Left/Right) - excluding Z and Y faces
        for x in {min_x, max_x}:
            for y in range(min_y + 1, max_y):
                for z in range(min_z + 1, max_z):
                    place_in_module(m, (x, y, z), block)
    return m


def Cylinder(base, radius, height, block, axis="y", fill=False):
    m = create_module("Cylinder")
    points = rasterize_cylinder(base, radius, height, axis, fill)
    for p in points:
        place_in_module(m, p, block)
    return m
