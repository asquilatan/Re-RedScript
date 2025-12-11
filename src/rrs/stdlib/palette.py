# Mapping of Block IDs to approx RGB values (averaged).
# Selection of colorful blocks and common materials.

BLOCK_PALETTE = {
    "minecraft:white_wool": (233, 236, 236),
    "minecraft:orange_wool": (240, 118, 19),
    "minecraft:magenta_wool": (189, 68, 179),
    "minecraft:light_blue_wool": (58, 175, 217),
    "minecraft:yellow_wool": (248, 197, 39),
    "minecraft:lime_wool": (112, 185, 25),
    "minecraft:pink_wool": (237, 141, 172),
    "minecraft:gray_wool": (62, 68, 71),
    "minecraft:light_gray_wool": (142, 142, 134),
    "minecraft:cyan_wool": (21, 137, 145),
    "minecraft:purple_wool": (121, 42, 172),
    "minecraft:blue_wool": (53, 57, 157),
    "minecraft:brown_wool": (114, 71, 40),
    "minecraft:green_wool": (84, 109, 27),
    "minecraft:red_wool": (161, 39, 34),
    "minecraft:black_wool": (20, 21, 25),

    "minecraft:white_concrete": (207, 213, 214),
    "minecraft:orange_concrete": (224, 97, 0),
    "minecraft:magenta_concrete": (169, 48, 159),
    "minecraft:light_blue_concrete": (35, 137, 198),
    "minecraft:yellow_concrete": (240, 175, 21),
    "minecraft:lime_concrete": (94, 169, 24),
    "minecraft:pink_concrete": (213, 101, 142),
    "minecraft:gray_concrete": (54, 57, 61),
    "minecraft:light_gray_concrete": (125, 125, 115),
    "minecraft:cyan_concrete": (21, 119, 136),
    "minecraft:purple_concrete": (100, 31, 156),
    "minecraft:blue_concrete": (44, 46, 143),
    "minecraft:brown_concrete": (96, 59, 31),
    "minecraft:green_concrete": (73, 91, 36),
    "minecraft:red_concrete": (142, 32, 32),
    "minecraft:black_concrete": (8, 10, 15),

    "minecraft:white_terracotta": (209, 177, 161),
    "minecraft:orange_terracotta": (160, 83, 37),
    "minecraft:magenta_terracotta": (149, 87, 108),
    "minecraft:light_blue_terracotta": (112, 108, 138),
    "minecraft:yellow_terracotta": (186, 133, 36),
    "minecraft:lime_terracotta": (103, 117, 53),
    "minecraft:pink_terracotta": (160, 77, 78),
    "minecraft:gray_terracotta": (57, 41, 35),
    "minecraft:light_gray_terracotta": (135, 107, 98),
    "minecraft:cyan_terracotta": (87, 92, 92),
    "minecraft:purple_terracotta": (118, 69, 86),
    "minecraft:blue_terracotta": (74, 60, 91),
    "minecraft:brown_terracotta": (77, 51, 35),
    "minecraft:green_terracotta": (76, 82, 42),
    "minecraft:red_terracotta": (142, 60, 46),
    "minecraft:black_terracotta": (37, 22, 16),
    "minecraft:terracotta": (150, 92, 66),

    "minecraft:gold_block": (250, 238, 77),
    "minecraft:diamond_block": (94, 233, 213),
    "minecraft:emerald_block": (46, 212, 116),
    "minecraft:lapis_block": (31, 67, 140),
    "minecraft:redstone_block": (148, 20, 0),
    "minecraft:coal_block": (19, 19, 19),
    "minecraft:iron_block": (192, 192, 192),

    "minecraft:prismarine": (99, 156, 151),
    "minecraft:dark_prismarine": (51, 91, 75),
    "minecraft:prismarine_bricks": (99, 171, 158),

    "minecraft:oak_planks": (162, 130, 78),
    "minecraft:spruce_planks": (114, 84, 56),
    "minecraft:birch_planks": (196, 177, 122),
    "minecraft:jungle_planks": (160, 115, 80),
    "minecraft:acacia_planks": (168, 90, 50),
    "minecraft:dark_oak_planks": (66, 43, 20),
    "minecraft:mangrove_planks": (120, 56, 47),
    "minecraft:cherry_planks": (224, 183, 176),
    "minecraft:crimson_planks": (101, 48, 70),
    "minecraft:warped_planks": (43, 104, 99),
    "minecraft:bamboo_planks": (225, 206, 121),

    "minecraft:stone": (125, 125, 125),
    "minecraft:cobblestone": (80, 80, 80),
    "minecraft:dirt": (134, 96, 67),
    "minecraft:sand": (219, 211, 160),
    "minecraft:red_sand": (190, 102, 31),
    "minecraft:gravel": (112, 108, 108),
    "minecraft:clay": (158, 164, 176),
    "minecraft:obsidian": (20, 18, 29),
    "minecraft:netherrack": (111, 54, 52),
    "minecraft:soul_sand": (81, 62, 50),
    "minecraft:end_stone": (221, 223, 165),
    "minecraft:sponge": (195, 192, 74),
    "minecraft:wet_sponge": (156, 153, 64),
    "minecraft:purpur_block": (169, 125, 169),

    "minecraft:snow_block": (249, 254, 254),
    "minecraft:ice": (159, 211, 252),
    "minecraft:packed_ice": (163, 188, 240),
    "minecraft:blue_ice": (116, 167, 253),

    "minecraft:acacia_log": (108, 99, 89),
    "minecraft:birch_log": (218, 218, 220),
    "minecraft:dark_oak_log": (60, 47, 39),
    "minecraft:jungle_log": (85, 67, 25),
    "minecraft:oak_log": (110, 85, 49),
    "minecraft:spruce_log": (59, 38, 20),
    "minecraft:stripped_acacia_log": (176, 92, 53),
    "minecraft:stripped_birch_log": (198, 178, 122),
    "minecraft:stripped_dark_oak_log": (67, 46, 26),
    "minecraft:stripped_jungle_log": (172, 126, 85),
    "minecraft:stripped_oak_log": (178, 145, 88),
    "minecraft:stripped_spruce_log": (116, 88, 56),

    "minecraft:hay_block": (172, 142, 28),
    "minecraft:tnt": (130, 41, 35),
    "minecraft:pumpkin": (208, 128, 38),
    "minecraft:melon": (131, 170, 48),

    # Concrete Powders
    "minecraft:white_concrete_powder": (226, 229, 229),
    "minecraft:orange_concrete_powder": (228, 129, 35),
    "minecraft:magenta_concrete_powder": (189, 79, 175),
    "minecraft:light_blue_concrete_powder": (75, 180, 211),
    "minecraft:yellow_concrete_powder": (233, 194, 58),
    "minecraft:lime_concrete_powder": (126, 188, 59),
    "minecraft:pink_concrete_powder": (230, 155, 176),
    "minecraft:gray_concrete_powder": (77, 81, 85),
    "minecraft:light_gray_concrete_powder": (154, 154, 148),
    "minecraft:cyan_concrete_powder": (37, 148, 157),
    "minecraft:purple_concrete_powder": (131, 57, 181),
    "minecraft:blue_concrete_powder": (70, 73, 166),
    "minecraft:brown_concrete_powder": (126, 84, 53),
    "minecraft:green_concrete_powder": (97, 119, 44),
    "minecraft:red_concrete_powder": (168, 54, 50),
    "minecraft:black_concrete_powder": (25, 27, 32),
}

from typing import Tuple
import functools

# Pre-process palette for faster lookup
# Convert keys to simple names if needed, but we used IDs.
PALETTE_LIST = [(color, block_id) for block_id, color in BLOCK_PALETTE.items()]

@functools.lru_cache(maxsize=1024)
def find_closest_block(rgb: Tuple[int, int, int]) -> str:
    """Finds the closest block ID for a given RGB color using Euclidean distance."""
    # This could be optimized (e.g., KD-Tree), but linear scan is fine for <1000 items and reasonable image sizes.
    best_dist = float('inf')
    best_block = "minecraft:stone" # Default

    r, g, b = rgb

    for color, block_id in PALETTE_LIST:
        pr, pg, pb = color
        dist = (r - pr)**2 + (g - pg)**2 + (b - pb)**2
        if dist < best_dist:
            best_dist = dist
            best_block = block_id

    return best_block
