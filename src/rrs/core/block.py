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

class AcaciaPlanks(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:acacia_planks", pos, **kwargs)

class ActivatorRail(Block):
    def __init__(self, pos=(0, 0, 0), shape='north_south', powered='false', **kwargs):
        super().__init__("minecraft:activator_rail", pos, shape=shape, powered=powered, **kwargs)

class BambooPlanks(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:bamboo_planks", pos, **kwargs)

class BirchPlanks(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:birch_planks", pos, **kwargs)

class BlackConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:black_concrete", pos, **kwargs)

class BlackGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:black_glazed_terracotta", pos, facing=facing, **kwargs)

class BlackStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:black_stained_glass", pos, **kwargs)

class BlackTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:black_terracotta", pos, **kwargs)

class BlueConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:blue_concrete", pos, **kwargs)

class BlueGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:blue_glazed_terracotta", pos, facing=facing, **kwargs)

class BlueStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:blue_stained_glass", pos, **kwargs)

class BlueTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:blue_terracotta", pos, **kwargs)

class BrownConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:brown_concrete", pos, **kwargs)

class BrownGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:brown_glazed_terracotta", pos, facing=facing, **kwargs)

class BrownStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:brown_stained_glass", pos, **kwargs)

class BrownTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:brown_terracotta", pos, **kwargs)

class CherryPlanks(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:cherry_planks", pos, **kwargs)

class Cobblestone(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:cobblestone", pos, **kwargs)

class Comparator(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', mode='compare', **kwargs):
        super().__init__("minecraft:comparator", pos, facing=facing, mode=mode, **kwargs)

class CyanConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:cyan_concrete", pos, **kwargs)

class CyanGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:cyan_glazed_terracotta", pos, facing=facing, **kwargs)

class CyanStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:cyan_stained_glass", pos, **kwargs)

class CyanTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:cyan_terracotta", pos, **kwargs)

class DarkOakPlanks(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:dark_oak_planks", pos, **kwargs)

class DaylightDetector(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:daylight_detector", pos, **kwargs)

class DetectorRail(Block):
    def __init__(self, pos=(0, 0, 0), shape='north_south', powered='false', **kwargs):
        super().__init__("minecraft:detector_rail", pos, shape=shape, powered=powered, **kwargs)

class DiamondBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:diamond_block", pos, **kwargs)

class Dirt(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:dirt", pos, **kwargs)

class Dispenser(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:dispenser", pos, facing=facing, **kwargs)

class Dropper(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:dropper", pos, facing=facing, **kwargs)

class EmeraldBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:emerald_block", pos, **kwargs)

class Glass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:glass", pos, **kwargs)

class Glowstone(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:glowstone", pos, **kwargs)

class GoldBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:gold_block", pos, **kwargs)

class GrassBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:grass_block", pos, **kwargs)

class Gravel(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:gravel", pos, **kwargs)

class GrayConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:gray_concrete", pos, **kwargs)

class GrayGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:gray_glazed_terracotta", pos, facing=facing, **kwargs)

class GrayStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:gray_stained_glass", pos, **kwargs)

class GrayTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:gray_terracotta", pos, **kwargs)

class GreenConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:green_concrete", pos, **kwargs)

class GreenGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:green_glazed_terracotta", pos, facing=facing, **kwargs)

class GreenStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:green_stained_glass", pos, **kwargs)

class GreenTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:green_terracotta", pos, **kwargs)

class HeavyWeightedPressurePlate(Block):
    def __init__(self, pos=(0, 0, 0), power=0, **kwargs):
        super().__init__("minecraft:heavy_weighted_pressure_plate", pos, power=power, **kwargs)

class HoneyBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:honey_block", pos, **kwargs)

class Hopper(Block):
    def __init__(self, pos=(0, 0, 0), facing='down', **kwargs):
        super().__init__("minecraft:hopper", pos, facing=facing, **kwargs)

class IronBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:iron_block", pos, **kwargs)

class JunglePlanks(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:jungle_planks", pos, **kwargs)

class LapisBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:lapis_block", pos, **kwargs)

class Lectern(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', has_book='false', **kwargs):
        super().__init__("minecraft:lectern", pos, facing=facing, has_book=has_book, **kwargs)

class Lever(Block):
    def __init__(self, pos=(0, 0, 0), face='wall', facing='north', powered='false', **kwargs):
        super().__init__("minecraft:lever", pos, face=face, facing=facing, powered=powered, **kwargs)

class LightBlueConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:light_blue_concrete", pos, **kwargs)

class LightBlueGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:light_blue_glazed_terracotta", pos, facing=facing, **kwargs)

class LightBlueStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:light_blue_stained_glass", pos, **kwargs)

class LightBlueTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:light_blue_terracotta", pos, **kwargs)

class LightGrayConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:light_gray_concrete", pos, **kwargs)

class LightGrayGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:light_gray_glazed_terracotta", pos, facing=facing, **kwargs)

class LightGrayStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:light_gray_stained_glass", pos, **kwargs)

class LightGrayTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:light_gray_terracotta", pos, **kwargs)

class LightWeightedPressurePlate(Block):
    def __init__(self, pos=(0, 0, 0), power=0, **kwargs):
        super().__init__("minecraft:light_weighted_pressure_plate", pos, power=power, **kwargs)

class LightningRod(Block):
    def __init__(self, pos=(0, 0, 0), facing='up', **kwargs):
        super().__init__("minecraft:lightning_rod", pos, facing=facing, **kwargs)

class LimeConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:lime_concrete", pos, **kwargs)

class LimeGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:lime_glazed_terracotta", pos, facing=facing, **kwargs)

class LimeStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:lime_stained_glass", pos, **kwargs)

class LimeTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:lime_terracotta", pos, **kwargs)

class MagentaConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:magenta_concrete", pos, **kwargs)

class MagentaGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:magenta_glazed_terracotta", pos, facing=facing, **kwargs)

class MagentaStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:magenta_stained_glass", pos, **kwargs)

class MagentaTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:magenta_terracotta", pos, **kwargs)

class MangrovePlanks(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:mangrove_planks", pos, **kwargs)

class NoteBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:note_block", pos, **kwargs)

class OakButton(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', face='wall', powered='false', **kwargs):
        super().__init__("minecraft:oak_button", pos, facing=facing, face=face, powered=powered, **kwargs)

class OakPlanks(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:oak_planks", pos, **kwargs)

class OakPressurePlate(Block):
    def __init__(self, pos=(0, 0, 0), powered='false', **kwargs):
        super().__init__("minecraft:oak_pressure_plate", pos, powered=powered, **kwargs)

class Observer(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:observer", pos, facing=facing, **kwargs)

class OrangeConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:orange_concrete", pos, **kwargs)

class OrangeGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:orange_glazed_terracotta", pos, facing=facing, **kwargs)

class OrangeStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:orange_stained_glass", pos, **kwargs)

class OrangeTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:orange_terracotta", pos, **kwargs)

class PinkConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:pink_concrete", pos, **kwargs)

class PinkGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:pink_glazed_terracotta", pos, facing=facing, **kwargs)

class PinkStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:pink_stained_glass", pos, **kwargs)

class PinkTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:pink_terracotta", pos, **kwargs)

class Piston(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:piston", pos, facing=facing, **kwargs)

class Podzol(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:podzol", pos, **kwargs)

class PoweredRail(Block):
    def __init__(self, pos=(0, 0, 0), shape='north_south', powered='false', **kwargs):
        super().__init__("minecraft:powered_rail", pos, shape=shape, powered=powered, **kwargs)

class PurpleConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:purple_concrete", pos, **kwargs)

class PurpleGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:purple_glazed_terracotta", pos, facing=facing, **kwargs)

class PurpleStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:purple_stained_glass", pos, **kwargs)

class PurpleTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:purple_terracotta", pos, **kwargs)

class Rail(Block):
    def __init__(self, pos=(0, 0, 0), shape='north_south', **kwargs):
        super().__init__("minecraft:rail", pos, shape=shape, **kwargs)

class RedConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:red_concrete", pos, **kwargs)

class RedGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:red_glazed_terracotta", pos, facing=facing, **kwargs)

class RedSand(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:red_sand", pos, **kwargs)

class RedStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:red_stained_glass", pos, **kwargs)

class RedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:red_terracotta", pos, **kwargs)

class RedstoneBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:redstone_block", pos, **kwargs)

class RedstoneLamp(Block):
    def __init__(self, pos=(0, 0, 0), lit='false', **kwargs):
        super().__init__("minecraft:redstone_lamp", pos, lit=lit, **kwargs)

class RedstoneTorch(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:redstone_torch", pos, **kwargs)

class RedstoneWire(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:redstone_wire", pos, **kwargs)

class Repeater(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', delay=1, **kwargs):
        super().__init__("minecraft:repeater", pos, facing=facing, delay=delay, **kwargs)

class Sand(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:sand", pos, **kwargs)

class SculkSensor(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:sculk_sensor", pos, **kwargs)

class SeaLantern(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:sea_lantern", pos, **kwargs)

class SlimeBlock(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:slime_block", pos, **kwargs)

class SprucePlanks(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:spruce_planks", pos, **kwargs)

class StickyPiston(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:sticky_piston", pos, facing=facing, **kwargs)

class Stone(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:stone", pos, **kwargs)

class StoneButton(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', face='wall', powered='false', **kwargs):
        super().__init__("minecraft:stone_button", pos, facing=facing, face=face, powered=powered, **kwargs)

class StonePressurePlate(Block):
    def __init__(self, pos=(0, 0, 0), powered='false', **kwargs):
        super().__init__("minecraft:stone_pressure_plate", pos, powered=powered, **kwargs)

class TNT(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:tnt", pos, **kwargs)

class Target(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:target", pos, **kwargs)

class Terracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:terracotta", pos, **kwargs)

class TintedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:tinted_glass", pos, **kwargs)

class TrappedChest(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:trapped_chest", pos, facing=facing, **kwargs)

class TripwireHook(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:tripwire_hook", pos, facing=facing, **kwargs)

class WhiteConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:white_concrete", pos, **kwargs)

class WhiteGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:white_glazed_terracotta", pos, facing=facing, **kwargs)

class WhiteStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:white_stained_glass", pos, **kwargs)

class WhiteTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:white_terracotta", pos, **kwargs)

class YellowConcrete(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:yellow_concrete", pos, **kwargs)

class YellowGlazedTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), facing='north', **kwargs):
        super().__init__("minecraft:yellow_glazed_terracotta", pos, facing=facing, **kwargs)

class YellowStainedGlass(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:yellow_stained_glass", pos, **kwargs)

class YellowTerracotta(Block):
    def __init__(self, pos=(0, 0, 0), **kwargs):
        super().__init__("minecraft:yellow_terracotta", pos, **kwargs)
