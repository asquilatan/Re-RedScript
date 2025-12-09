from typing import List, Tuple, Dict, Any, Optional, Union
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
        # Block registry for name-based access
        self._block_registry: Dict[str, 'Module'] = {}
        # Variable registry for module attribute access (exports)
        self.exports: Dict[str, Any] = {}
        # Optional trigger callback
        self.trigger = None

    def add(self, module: 'Module'):
        """Add a child module."""
        self.children.append(module)

    def register_block(self, name: str, block: 'Module'):
        """Register a block by name for later access via m.block_name"""
        self._block_registry[name] = block

    def get_block(self, pos: Tuple[int, int, int]) -> Optional['Module']:
        """Get a block by position"""
        for child in self.children:
            if hasattr(child, 'pos') and child.pos == pos:
                return child
        return None

    def __getattr__(self, name: str):
        """Allow access to registered blocks and exported variables"""
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        if name in self._block_registry:
            return self._block_registry[name]
        if name in self.exports:
            return self.exports[name]
        raise AttributeError(f"Module '{self.id}' has no attribute named '{name}'")

    def __getitem__(self, key: Union[str, List[str]]) -> Union['Module', List['Module']]:
        """Allow indexing: m['block'] or m[b1, b2, b3]"""
        if isinstance(key, str):
            return self._block_registry.get(key)
        elif isinstance(key, (list, tuple)):
            return [self._block_registry.get(k) for k in key if k in self._block_registry]
        raise TypeError(f"Module indices must be str or list of str, not {type(key)}")

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
