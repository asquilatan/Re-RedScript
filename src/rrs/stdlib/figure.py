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

    xs = range(min(x1, x2), max(x1, x2) + 1)
    ys = range(min(y1, y2), max(y1, y2) + 1)
    zs = range(min(z1, z2), max(z1, z2) + 1)

    for x in xs:
        for y in ys:
            for z in zs:
                is_border = (x == x1 or x == x2 or y == y1 or y == y2 or z == z1 or z == z2)
                if fill or is_border:
                    place_in_module(m, (x,y,z), block)
    return m

def Cylinder(base, radius, height, block, axis='y', fill=False):
    m = create_module("Cylinder")
    points = rasterize_cylinder(base, radius, height, axis, fill)
    for p in points:
        place_in_module(m, p, block)
    return m
