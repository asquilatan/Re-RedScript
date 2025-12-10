from typing import List, Tuple, Union, Dict, Any
from rrs.core.block import Block
from rrs.core.module import Module
from rrs.stdlib.geometry import bresenham_line, bezier_curve, rasterize_sphere, rasterize_cylinder, catmull_rom_spline
from rrs.stdlib.utils import create_module, place_in_module, WeightedBlock
import rrs.stdlib.line as line
import rrs.stdlib.figure as figure

class StdLib:
    """Standard Library for Re-RedScript containing geometry and utility functions.
       Deprecated: Use std.line, std.figure, etc. instead.
    """
    
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def Line(self, start, end, block, thickness=1):
        return line.Line(start, end, block, thickness)

    def Path(self, points: List[Tuple[int, int, int]], block, thickness=1, closed=False, smooth=False):
        return line.Path(points, block, thickness, closed, smooth)

    def Bezier(self, start, c1, c2, end, block, segments=20, thickness=1):
        return line.Bezier(start, c1, c2, end, block, segments, thickness)

    def Sphere(self, center, radius, block, fill=False):
        return figure.Sphere(center, radius, block, fill)
        
    def Cuboid(self, pos1, pos2, block, fill=False):
        return figure.Cuboid(pos1, pos2, block, fill)

    def Cylinder(self, base, radius, height, block, axis='y', fill=False):
        return figure.Cylinder(base, radius, height, block, axis, fill)

    def Weighted(self, weights):
        return WeightedBlock(weights)
