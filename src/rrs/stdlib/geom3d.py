from typing import List, Tuple, Union, Dict, Any, Type
from rrs.core.block import Block
from rrs.core.module import Module
from rrs.stdlib.geometry import rasterize_sphere, rasterize_cylinder

class Geom3D:
    """Standard Library for 3D Geometry (Solids, Shapes)."""

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def _resolve_block(self, block_or_weighted):
        if hasattr(block_or_weighted, 'pick'):
            return block_or_weighted.pick()
        return block_or_weighted

    def _create_module(self, name):
        return Module(name)

    def _place_in_module(self, module: Module, pos: Tuple[int, int, int], block_or_weighted):
        import copy
        final_block = self._resolve_block(block_or_weighted)

        if isinstance(final_block, type) and issubclass(final_block, Block):
             instance = final_block(pos=pos)
             module.add(instance)
             return instance

        elif isinstance(final_block, Block):
             instance = type(final_block)(pos=pos, **final_block.properties)
             module.add(instance)
             return instance

        elif isinstance(final_block, str):
             instance = Block(final_block, pos=pos)
             module.add(instance)
             return instance

        elif isinstance(final_block, Module):
            instance = copy.deepcopy(final_block)
            instance.pos = pos
            module.add(instance)
            return instance

        elif callable(final_block):
            try:
                instance = final_block(pos=pos)
            except TypeError:
                try:
                    instance = final_block()
                    if hasattr(instance, 'pos'):
                        instance.pos = pos
                except Exception:
                    return None

            if instance:
                module.add(instance)
                return instance

        return None

    def Sphere(self, center, radius, block, fill=False):
        """Draws a sphere."""
        m = self._create_module("Sphere")
        points = rasterize_sphere(center, radius, fill)
        for p in points:
            self._place_in_module(m, p, block)
        return m

    def Cuboid(self, pos1, pos2, block, fill=False):
        """Draws a cuboid defined by two opposite corners."""
        m = self._create_module("Cuboid")
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
                        self._place_in_module(m, (x,y,z), block)
        return m

    def Cylinder(self, base, radius, height, block, axis='y', fill=False):
        """Draws a cylinder."""
        m = self._create_module("Cylinder")
        points = rasterize_cylinder(base, radius, height, axis, fill)
        for p in points:
            self._place_in_module(m, p, block)
        return m
