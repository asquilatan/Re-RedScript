import json
import os
from typing import List, Tuple, Dict, Any, Type
from rrs.core.module import Module
from rrs.utils.math import add_vec3

class Block(Module):
    """Represents a single Minecraft block."""

    def __init__(self, id: str, pos: Tuple[int, int, int] = (0, 0, 0), **kwargs):
        super().__init__(id, pos, size=(1, 1, 1), **kwargs)

    def flatten(self, offset: Tuple[int, int, int] = (0, 0, 0)) -> List['Module']:
        """Returns a list containing a copy of this block with absolute position."""
        results: List['Module'] = []
        self._flatten_into(offset, results)
        return results

    def _flatten_into(self, offset: Tuple[int, int, int], accumulator: List['Module']):
        """Internal helper to flatten into an existing list."""
        new_block = self.__class__.__new__(self.__class__)
        new_block.__dict__ = self.__dict__.copy()
        new_block.pos = add_vec3(self.pos, offset)
        accumulator.append(new_block)

def create_block_class(name: str, block_def: Dict[str, Any]) -> Type[Block]:
    """Dynamically creates a Block subclass from a definition."""
    block_id = block_def["id"]
    defaults = block_def.get("defaults", {})
    
    def __init__(self, pos=(0, 0, 0), **kwargs):
        # Merge defaults with kwargs
        final_kwargs = defaults.copy()
        final_kwargs.update(kwargs)
        Block.__init__(self, block_id, pos, **final_kwargs)
        
    new_class = type(name, (Block,), {"__init__": __init__})
    return new_class

def load_blocks_from_json(json_path: str) -> Dict[str, Type[Block]]:
    """Loads block definitions from a JSON file and returns a dict of classes."""
    if not os.path.exists(json_path):
        return {}
        
    with open(json_path, 'r', encoding='utf-8') as f:
        blocks_data = json.load(f)
        
    loaded_blocks = {}
    for name, data in blocks_data.items():
        loaded_blocks[name] = create_block_class(name, data)
        
    return loaded_blocks
