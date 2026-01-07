from typing import Optional, Tuple
from PIL import Image
from rrs.stdlib.utils import create_module, place_in_module
from rrs.stdlib.palette import find_closest_block, PALETTE_LIST
import math
import numpy as np

def ConvertPicture(path: str, length: Optional[int] = None, width: Optional[int] = None, height: int = 1, vertical: bool = False, rotate: float = 0, heightmap: bool = False):
    """
    Converts an image file to a Module of blocks.

    Args:
        path: Path to the image file.
        length: Desired length (X axis size usually) in blocks. Resizes image if provided.
        width: Desired width (Z axis size usually) in blocks. Resizes image if provided.
        height:
            If heightmap=False: The height (Y axis) of the stacked image extrusion.
            If heightmap=True: The maximum height of the terrain generation.
        vertical: If True, generates the image upright (XY plane). If False (default), generates flat (XZ plane).
        rotate: Rotation angle in degrees (clockwise).
        heightmap: If True, uses brightness for Y-height.

    Returns:
        A Module containing the blocks.
    """
    m = create_module("Picture")

    try:
        img = Image.open(path)
    except IOError:
        # In case path is relative to script execution or some other issue
        print(f"Warning: Could not load image at {path}")
        return m

    img = img.convert("RGB")

    # 1. Handle Rotate
    if rotate != 0:
        img = img.rotate(-rotate, expand=True) # Negative because PIL rotates counter-clockwise

    # 2. Handle Resize
    target_w, target_h = img.size

    if length is not None and width is not None:
        target_w, target_h = int(length), int(width)
    elif length is not None:
        ratio = length / float(img.size[0])
        target_w = int(length)
        target_h = int(img.size[1] * ratio)
    elif width is not None:
        ratio = width / float(img.size[1])
        target_w = int(img.size[0] * ratio)
        target_h = int(width)

    if (target_w, target_h) != img.size:
        img = img.resize((target_w, target_h), Image.Resampling.NEAREST)

    # Optimization: Use Numpy for vectorized color matching
    img_array = np.array(img) # (h, w, 3)

    # Prepare palette
    palette_colors = np.array([c for c, _ in PALETTE_LIST]) # (P, 3)
    palette_blocks = [b for _, b in PALETTE_LIST]

    # Flatten image for processing
    h, w, _ = img_array.shape
    pixels_flat = img_array.reshape(-1, 3) # (N, 3)

    # Vectorized Euclidean distance calculation
    # (a-b)^2 = a^2 + b^2 - 2ab
    pixels_float = pixels_flat.astype(float)
    palette_float = palette_colors.astype(float)

    palette_sum_sq = np.sum(palette_float**2, axis=1) # (P,)

    dot_prod = np.dot(pixels_float, palette_float.T) # (N, P)

    # Optimization: Omit pixel_sum_sq as it's constant per row and doesn't affect argmin order
    dists = palette_sum_sq[np.newaxis, :] - 2 * dot_prod

    closest_indices = np.argmin(dists, axis=1) # (N,)

    # Now iterate and place blocks
    for idx, best_idx in enumerate(closest_indices):
        px = idx % w
        py = idx // w

        block_id = palette_blocks[best_idx]
        color = pixels_flat[idx] # uint8 array

        # Map image (x, y) to module (x, y, z)
        # Default (Horizontal, flat on ground): Image X -> Module X, Image Y -> Module Z
        # Vertical (Upright): Image X -> Module X, Image Y -> Module Y

        ix, iy = px, py

        if heightmap:
            # Use brightness for height
            # Brightness = (R+G+B)/3 or using luminance formula
            # Normalize to 0..height
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            brightness = (r + g + b) / (3.0 * 255.0)
            # Map 0..1 to 1..height (or 0..height-1?)
            # Assuming height=1 means flat. height=10 means max height 10.
            y_offset = int(brightness * (height - 1)) if height > 1 else 0

            if vertical:
                # Heightmap on vertical plane? "Terrain" usually implies XZ plane.
                # But if vertical=True, maybe it's a relief map on a wall.
                # Wall is on XY plane. Depth/Relief is Z axis.
                # Let's implement that.
                # Base pos: (ix, iy, 0). Extrude to (ix, iy, y_offset)
                # Or just place block at (ix, iy, y_offset)? "get a heightmap... use that to determine the height"
                # Usually means solid column or surface.
                # Let's place a column from 0 to y_offset? Or just the surface?
                # "blocks should still use the color of the pixel"
                # I'll generate a solid column of that block.
                for z in range(y_offset + 1):
                        place_in_module(m, (ix, h - 1 - iy, z), block_id) # Flip Y for image coords
            else:
                # Standard terrain (XZ plane, height is Y)
                for y in range(y_offset + 1):
                    place_in_module(m, (ix, y, iy), block_id)

        else:
            # Not a heightmap. Stacking.
            # If vertical:
            #   X -> X
            #   Y -> Y (Image Y usually goes down, Minecraft Y goes up. Flip it?)
            #   Z -> Stack depth

            # If horizontal:
            #   X -> X
            #   Y -> Z
            #   Z -> Stack height (Y)

            if vertical:
                # Image (x,y) -> Module (x,y). Stack on Z.
                # Flip image Y to match standard coordinate systems (bottom-left origin vs top-left)
                # Minecraft: Y is up. Image: Y is down.
                pos_x = ix
                pos_y = h - 1 - iy

                for z in range(height):
                    place_in_module(m, (pos_x, pos_y, z), block_id)
            else:
                # Image (x,y) -> Module (x, z). Stack on Y.
                pos_x = ix
                pos_z = iy

                for y in range(height):
                    place_in_module(m, (pos_x, y, pos_z), block_id)

    return m
