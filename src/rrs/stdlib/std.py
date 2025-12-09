import random
from typing import List, Tuple, Union, Dict, Any
from rrs.core.block import Block
from rrs.core.module import Module
from rrs.stdlib.geometry import bresenham_line, bezier_curve, rasterize_sphere, rasterize_cylinder, catmull_rom_spline

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
    """Standard Library for Re-RedScript containing geometry and utility functions."""
    
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def _resolve_block(self, block_or_weighted):
        if isinstance(block_or_weighted, WeightedBlock):
            return block_or_weighted.pick()
        return block_or_weighted

    def _create_module(self, name):
        """Helper to create a module."""
        # If we can use the interpreter's create_module (which might handle scope), good.
        # Otherwise instantiating Module directly works but might miss some metadata.
        # Since these are transient modules returned by functions, instantiating directly is cleaner.
        return Module(name)

    def _place_in_module(self, module: Module, pos: Tuple[int, int, int], block_or_weighted):
        """Places a block at a position in a specific module."""
        import copy
        final_block = self._resolve_block(block_or_weighted)
        
        # 1. Block Class (Factory)
        if isinstance(final_block, type) and issubclass(final_block, Block):
             instance = final_block(pos=pos)
             module.add(instance)
             return instance
             
        # 2. Block Instance
        elif isinstance(final_block, Block):
             instance = type(final_block)(pos=pos, **final_block.properties)
             module.add(instance)
             return instance
             
        # 3. String (Block ID)
        elif isinstance(final_block, str):
             # Create simple block
             instance = Block(final_block, pos=pos)
             module.add(instance)
             return instance

        # 4. Module Instance (Clone it)
        elif isinstance(final_block, Module):
            # Clone to separate scope/instance
            # Using deepcopy to ensure blocks inside are new instances
            instance = copy.deepcopy(final_block)
            instance.pos = pos
            module.add(instance)
            return instance

        # 5. Callable (Module Factory / Custom Function)
        elif callable(final_block):
            # Try to call it with pos kwarg, if that fails, try without
            try:
                instance = final_block(pos=pos)
            except TypeError:
                # Assuming simple factory call, set pos after?
                # Or maybe it doesn't take args.
                try:
                    instance = final_block()
                    if hasattr(instance, 'pos'):
                        instance.pos = pos
                except Exception:
                    # If it fails, we can't do much
                    return None
            
            if instance:
                module.add(instance)
                return instance

        return None

    def Line(self, start, end, block, thickness=1):
        m = self._create_module("Line")
        points = bresenham_line(start, end)
        
        for p in points:
            if thickness <= 1:
                self._place_in_module(m, p, block)
            else:
                sphere_points = rasterize_sphere(p, thickness/2, fill=True)
                for sp in sphere_points:
                    self._place_in_module(m, sp, block)
                    
        # If called as a standalone statement (not assigned), we might want to auto-add to parent?
        # User requirement: "calling the function will give a module object"
        # RRS Standard: If an expression evaluates to a Module and is a statement, it is AUTO-ADDED if it's a call?
        # If `Line(...)` is 8 blocks, we return a Module containing 8 blocks.
        # If the user just writes `Line(...)`, that Module is created but maybe not added to the current scope?
        # In RRS `FunctionCall` can be an expression or statement.
        # If it's a statement, the return value is discarded unless we handle it?
        # Wait, if `Line` returns a Module, and I write `Line(...)`, I expect the line to appear.
        # So we should probably ALSO add it to the current module if one exists?
        # OR, better: The function RETURNS a module, but the Interpreter handles auto-adding?
        # In standard RRS: `Block(...)` returns a Block. If unchecked, it's garbage collected.
        # But `Std.Line` is typically used for side effects.
        # However, the user explicitly asked for "modules right off the bat".
        # Let's align with RRS IDIOM:
        # Calls that return Modules are usually instantiations. `MyMod()` returns a module.
        # If `MyMod()` is a statement, the interpreter calls `current_module.add(result)`.
        # So we just return the Module, and let the Interpreter handle the adding!
        return m

    def Path(self, points: List[Tuple[int, int, int]], block, thickness=1, closed=False, smooth=False):
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
        m = self._create_module("Bezier")
        points = bezier_curve([start, c1, c2, end], segments)
        for p in points:
             self._place_in_module(m, p, block)
        return m

    def Sphere(self, center, radius, block, fill=False):
        m = self._create_module("Sphere")
        points = rasterize_sphere(center, radius, fill)
        for p in points:
            self._place_in_module(m, p, block)
        return m
        
    def Cuboid(self, pos1, pos2, block, fill=False):
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
        m = self._create_module("Cylinder")
        points = rasterize_cylinder(base, radius, height, axis, fill)
        for p in points:
            self._place_in_module(m, p, block)
        return m

    def Weighted(self, weights):
        return WeightedBlock(weights)
