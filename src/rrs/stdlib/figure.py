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

    x_min, x_max = sorted((x1, x2))
    y_min, y_max = sorted((y1, y2))
    z_min, z_max = sorted((z1, z2))

    if fill:
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    place_in_module(m, (x, y, z), block)
    else:
        # Optimized hollow cuboid generation: iterate only over faces
        # 1. Z-faces (Top/Bottom)
        for z in {z_min, z_max}:
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    place_in_module(m, (x, y, z), block)

        # 2. Y-faces (Front/Back), excluding Z-faces
        for y in {y_min, y_max}:
            for x in range(x_min, x_max + 1):
                for z in range(z_min + 1, z_max):
                    place_in_module(m, (x, y, z), block)

        # 3. X-faces (Left/Right), excluding Z and Y faces
        for x in {x_min, x_max}:
            for y in range(y_min + 1, y_max):
                for z in range(z_min + 1, z_max):
                    place_in_module(m, (x, y, z), block)

    return m


def Cylinder(base, radius, height, block, axis='y', fill=False):
    m = create_module("Cylinder")
    points = rasterize_cylinder(base, radius, height, axis, fill)
    for p in points:
        place_in_module(m, p, block)
    return m
