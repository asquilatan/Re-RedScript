import random
from typing import List, Tuple, Union, Dict, Any
from rrs.core.block import Block
from rrs.core.module import Module
from rrs.stdlib.geom2d import Geom2D
from rrs.stdlib.geom3d import Geom3D

class WeightedBlock:
    def __init__(self, weights: Union[Dict[Any, float], List[Tuple[Any, float]]]):
        if isinstance(weights, dict):
            self.choices = list(weights.keys())
            self.weights = list(weights.values())
        else:
             self.choices = [w[0] for w in weights]
             self.weights = [w[1] for w in weights]

    def pick(self):
        return random.choices(self.choices, weights=self.weights, k=1)[0]

class StdLib:
    """Standard Library for Re-RedScript containing geometry and utility functions.

    DEPRECATED: This module is deprecated. Use std.geom2d and std.geom3d instead.
    """
    
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.geom2d = Geom2D(interpreter)
        self.geom3d = Geom3D(interpreter)
        print("Warning: The 'std' module is deprecated. Please migrate to 'std.geom2d' and 'std.geom3d'.")

    def Weighted(self, weights):
        return WeightedBlock(weights)

    # Proxy methods to Geom2D
    def Line(self, *args, **kwargs):
        return self.geom2d.Line(*args, **kwargs)

    def Path(self, *args, **kwargs):
        return self.geom2d.Path(*args, **kwargs)

    def Bezier(self, *args, **kwargs):
        return self.geom2d.Bezier(*args, **kwargs)

    # Proxy methods to Geom3D
    def Sphere(self, *args, **kwargs):
        return self.geom3d.Sphere(*args, **kwargs)

    def Cuboid(self, *args, **kwargs):
        return self.geom3d.Cuboid(*args, **kwargs)

    def Cylinder(self, *args, **kwargs):
        return self.geom3d.Cylinder(*args, **kwargs)
