from typing import List, Tuple
from rrs.core.module import Module
from rrs.utils.math import add_vec3
import copy

class Block(Module):
    """
    Represents a single Minecraft block.
    """
    def __init__(self, id: str, pos: Tuple[int, int, int] = (0, 0, 0), **kwargs):
        super().__init__(id, pos, size=(1, 1, 1), **kwargs)
    
    def flatten(self, offset: Tuple[int, int, int] = (0, 0, 0)) -> List['Module']:
        # Return a copy of self with absolute position
        new_block = copy.copy(self)
        new_block.pos = add_vec3(self.pos, offset)
        return [new_block]

# Standard Minecraft Blocks

class Stone(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:stone", pos, **kwargs)

class Piston(Block):
    def __init__(self, pos=(0, 0, 0), facing="north", **kwargs):
        super().__init__("minecraft:piston", pos, facing=facing, **kwargs)

class Repeater(Block):
    def __init__(self, pos=(0, 0, 0), facing="north", delay=1, **kwargs):
        super().__init__("minecraft:repeater", pos, facing=facing, delay=delay, **kwargs)

# Decorative Blocks
class GoldBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:gold_block", pos, **kwargs)

class DiamondBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:diamond_block", pos, **kwargs)

class EmeraldBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:emerald_block", pos, **kwargs)

class Glowstone(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:glowstone", pos, **kwargs)

class SeaLantern(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:sea_lantern", pos, **kwargs)

class RedstoneBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:redstone_block", pos, **kwargs)

class LapisBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:lapis_block", pos, **kwargs)

class IronBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:iron_block", pos, **kwargs)

class Observer(Block):
    def __init__(self, pos=(0, 0, 0), facing="north", **kwargs):
        super().__init__("minecraft:observer", pos, facing=facing, **kwargs)
