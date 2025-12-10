from typing import Optional, Tuple
from PIL import Image
from rrs.stdlib.utils import create_module, place_in_module
from rrs.stdlib.palette import find_closest_block
import math

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
    # Determine target size
    # If user provided length/width, force resize.
    # If user provided one, scale proportionally? The prompt says "length and width should resize the dimensions".
    # Assuming if both provided, non-uniform scale. If one, uniform?
    # Prompt: "The length and with should resize the dimensions of the image"
    # "defaults to l and w of image"

    target_w, target_h = img.size # PIL uses (width, height) which maps to (x, y) usually

    if length is not None and width is not None:
        target_w, target_h = int(length), int(width)
    elif length is not None:
        # Scale width to length, keep aspect ratio?
        # Usually length maps to X. Width maps to Z (or Y in image terms).
        # Let's assume length -> image width, width -> image height.
        ratio = length / float(img.size[0])
        target_w = int(length)
        target_h = int(img.size[1] * ratio)
    elif width is not None:
        ratio = width / float(img.size[1])
        target_w = int(img.size[0] * ratio)
        target_h = int(width)

    if (target_w, target_h) != img.size:
        img = img.resize((target_w, target_h), Image.Resampling.NEAREST)

    pixels = img.load()
    w, h = img.size

    # Iterate pixels
    # Image coordinates: x (0..w-1), y (0..h-1)

    for px in range(w):
        for py in range(h):
            color = pixels[px, py]
            block_id = find_closest_block(color)

            # Map image (x, y) to module (x, y, z)
            # Default (Horizontal, flat on ground): Image X -> Module X, Image Y -> Module Z
            # Vertical (Upright): Image X -> Module X, Image Y -> Module Y

            ix, iy = px, py

            if heightmap:
                # Use brightness for height
                # Brightness = (R+G+B)/3 or using luminance formula
                # Normalize to 0..height
                r, g, b = color
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
