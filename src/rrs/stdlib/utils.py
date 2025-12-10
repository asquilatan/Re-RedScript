from typing import Tuple, Union, Dict, Any, List
from rrs.core.block import Block
from rrs.core.module import Module
import copy
import random

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

def resolve_block(block_or_weighted):
    if isinstance(block_or_weighted, WeightedBlock):
        return block_or_weighted.pick()
    return block_or_weighted

def create_module(name: str):
    """Helper to create a module."""
    return Module(name)

def place_in_module(module: Module, pos: Tuple[int, int, int], block_or_weighted):
    """Places a block at a position in a specific module."""
    final_block = resolve_block(block_or_weighted)

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
