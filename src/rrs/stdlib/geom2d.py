from typing import List, Tuple, Union, Dict, Any, Type
from rrs.core.block import Block
from rrs.core.module import Module
from rrs.stdlib.geometry import bresenham_line, bezier_curve, catmull_rom_spline

class Geom2D:
    """Standard Library for 2D Geometry (Lines, Curves, Paths)."""

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def _resolve_block(self, block_or_weighted):
        # We can re-use logic from old StdLib or just import a helper.
        # Duplicating small helper is fine to avoid tight coupling.
        if hasattr(block_or_weighted, 'pick'): # WeightedBlock
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

    def Line(self, start, end, block, thickness=1):
        """Draws a line between two points."""
        m = self._create_module("Line")
        points = bresenham_line(start, end)

        # Need rasterize_sphere for thickness, importing here to keep it self-contained or import at top
        from rrs.stdlib.geometry import rasterize_sphere

        for p in points:
            if thickness <= 1:
                self._place_in_module(m, p, block)
            else:
                sphere_points = rasterize_sphere(p, thickness/2, fill=True)
                for sp in sphere_points:
                    self._place_in_module(m, sp, block)
        return m

    def Path(self, points: List[Tuple[int, int, int]], block, thickness=1, closed=False, smooth=False):
        """Draws a path connecting multiple points."""
        m = self._create_module("Path")
        if len(points) < 2: return m

        path_points = points
        if closed:
            path_points = points + [points[0]]

        if smooth:
            spline_points = catmull_rom_spline(path_points, segments=10)
            for p in spline_points:
                 self._place_in_module(m, p, block)
        else:
            for i in range(len(path_points) - 1):
                seg_points = bresenham_line(path_points[i], path_points[i+1])
                for p in seg_points:
                    self._place_in_module(m, p, block)
        return m

    def Bezier(self, start, c1, c2, end, block, segments=20, thickness=1):
        """Draws a cubic Bezier curve."""
        m = self._create_module("Bezier")
        points = bezier_curve([start, c1, c2, end], segments)
        for p in points:
             self._place_in_module(m, p, block)
        return m
