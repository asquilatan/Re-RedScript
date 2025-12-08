from typing import List, Tuple, Dict, Any
from rrs.utils.math import add_vec3

class Module:
    """
    Base unit of construction in Re-RedScript.
    """
    def __init__(
        self, 
        id: str, 
        pos: Tuple[int, int, int] = (0, 0, 0), 
        size: Tuple[int, int, int] = (1, 1, 1),
        **kwargs
    ):
        self.id = id
        self.pos = pos
        self.size = size
        self.children: List['Module'] = []
        self.properties: Dict[str, Any] = kwargs

    def add(self, module: 'Module'):
        """Add a child module."""
        self.children.append(module)

    def __iadd__(self, module: 'Module'):
        self.add(module)
        return self

    def flatten(self, offset: Tuple[int, int, int] = (0, 0, 0)) -> List['Module']:
        """
        Recursively flatten the module hierarchy into a list of blocks with absolute positions.
        """
        absolute_pos = add_vec3(self.pos, offset)
        flat_list = []
        for child in self.children:
            flat_list.extend(child.flatten(absolute_pos))
        return flat_list
