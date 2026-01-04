from typing import List, Tuple, Dict, Any, Optional, Union
from rrs.utils.math import add_vec3

class Module:
    """Base unit of construction in Re-RedScript.

    A Module is a container for blocks and other modules, forming a hierarchical structure.
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
        self._block_registry: Dict[str, 'Module'] = {}
        self.exports: Dict[str, Any] = {}
        self.trigger = None

    def add(self, module: 'Module'):
        """Adds a child module or block to this module."""
        self.children.append(module)

    def register_block(self, name: str, block: 'Module'):
        """Registers a block by name for later access."""
        self._block_registry[name] = block

    def get_block(self, pos: Tuple[int, int, int]) -> Optional['Module']:
        """Returns a block at the specified relative position."""
        for child in self.children:
            if hasattr(child, 'pos') and child.pos == pos:
                return child
        return None

    def __getattr__(self, name: str):
        """Allows access to registered blocks and exported variables."""
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        if name in self._block_registry:
            return self._block_registry[name]
        if name in self.exports:
            return self.exports[name]
        raise AttributeError(f"Module '{self.id}' has no attribute named '{name}'")

    def __getitem__(self, key: Union[str, List[str]]) -> Union['Module', List['Module']]:
        """Allows indexing to retrieve registered blocks."""
        if isinstance(key, str):
            return self._block_registry.get(key)
        elif isinstance(key, (list, tuple)):
            return [self._block_registry.get(k) for k in key if k in self._block_registry]
        raise TypeError(f"Module indices must be str or list of str, not {type(key)}")

    def __iadd__(self, module: 'Module'):
        self.add(module)
        return self

    def flatten(self, offset: Tuple[int, int, int] = (0, 0, 0)) -> List['Module']:
        """Recursively flattens the module hierarchy into a list of blocks with absolute positions."""  # noqa: E501
        results: List['Module'] = []
        self._flatten_into(offset, results)
        return results

    def _flatten_into(self, offset: Tuple[int, int, int], accumulator: List['Module']):
        """Internal helper to flatten into an existing list."""
        absolute_pos = add_vec3(self.pos, offset)
        for child in self.children:
            # Check for _flatten_into to allow duck typing if needed,
            # though usually all children are Modules.
            if hasattr(child, '_flatten_into'):
                child._flatten_into(absolute_pos, accumulator)
            else:
                accumulator.extend(child.flatten(absolute_pos))
