# Mapping of Minecraft block IDs to average RGB color.
# Sources: approximate average colors.

PALETTE = {
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
    "minecraft:orange_terracotta": (159, 82, 36),
    "minecraft:magenta_terracotta": (149, 87, 108),
    "minecraft:light_blue_terracotta": (112, 108, 138),
    "minecraft:yellow_terracotta": (186, 133, 36),
    "minecraft:lime_terracotta": (103, 117, 53),
    "minecraft:pink_terracotta": (160, 77, 78),
    "minecraft:gray_terracotta": (57, 41, 35),
    "minecraft:light_gray_terracotta": (135, 107, 98),
    "minecraft:cyan_terracotta": (87, 92, 92),
    "minecraft:purple_terracotta": (118, 69, 86),
    "minecraft:blue_terracotta": (74, 59, 91),
    "minecraft:brown_terracotta": (77, 51, 35),
    "minecraft:green_terracotta": (76, 82, 42),
    "minecraft:red_terracotta": (142, 60, 46),
    "minecraft:black_terracotta": (37, 22, 16),

    # "minecraft:gold_block": (246, 208, 61),
    # "minecraft:iron_block": (220, 220, 220),
    # "minecraft:diamond_block": (98, 237, 228),
    # "minecraft:emerald_block": (65, 243, 132),
    # "minecraft:lapis_block": (38, 67, 137),
    # "minecraft:redstone_block": (172, 23, 12),
}

from typing import Tuple

def get_closest_block(rgb: Tuple[int, int, int]) -> str:
    """Finds the block ID with the color closest to the given RGB tuple."""
    r, g, b = rgb
    best_dist = float('inf')
    best_block = "minecraft:stone" # Default fallback

    for block_id, (br, bg, bb) in PALETTE.items():
        # Euclidean distance
        dist = (r - br) ** 2 + (g - bg) ** 2 + (b - bb) ** 2
        if dist < best_dist:
            best_dist = dist
            best_block = block_id

    return best_block
