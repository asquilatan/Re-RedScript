from typing import Optional, Tuple
from PIL import Image
from rrs.core.module import Module
from rrs.core.block import Block
from rrs.stdlib.palette import get_closest_block

class ImgLib:
    """Standard Library for Image processing (PNG to Blocks)."""

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def ConvertPicture(self, path: str, length: Optional[int] = None, width: Optional[int] = None, height: int = 1):
        """
        Converts an image to a module of blocks.

        Args:
            path: Path to the image file.
            length: Target width (X axis) in blocks. If None, uses image width.
            width: Target depth (Z axis) in blocks. If None, uses image height (Z).
                   Note: We map Image X -> X, Image Y -> Z (flat on ground).
            height: Thickness (Y axis) of the image. Defaults to 1.
        """
        try:
            img = Image.open(path)
        except Exception as e:
            print(f"Error opening image {path}: {e}")
            return Module("Error")

        img = img.convert("RGB")
        orig_w, orig_h = img.size

        target_w = length if length is not None else orig_w
        target_h = width if width is not None else orig_h # Map image Y to Z (width)

        if target_w != orig_w or target_h != orig_h:
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        # Create module
        m = Module("ConvertPicture")

        pixels = img.load()
        for x in range(target_w):
            for z in range(target_h): # Image Y -> World Z
                r, g, b = pixels[x, z]
                block_id = get_closest_block((r, g, b))

                # Extrude vertically
                for y in range(height):
                    blk = Block(block_id, pos=(x, y, z))
                    m.add(blk)

        return m

    def ConvertHeightmap(self, path: str, length: Optional[int] = None, width: Optional[int] = None, max_height: int = 10, base_height: int = 1):
        """
        Converts an image to a 3D terrain heightmap.
        Brightness determines height. Color determines block.

        Args:
            path: Path to the image.
            length: Target X size.
            width: Target Z size.
            max_height: Maximum height of the terrain (added to base_height).
            base_height: Minimum height.
        """
        try:
            img = Image.open(path)
        except Exception as e:
            print(f"Error opening image {path}: {e}")
            return Module("Error")

        img = img.convert("RGB")
        orig_w, orig_h = img.size

        target_w = length if length is not None else orig_w
        target_h = width if width is not None else orig_h

        if target_w != orig_w or target_h != orig_h:
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        m = Module("ConvertHeightmap")
        pixels = img.load()

        for x in range(target_w):
            for z in range(target_h):
                r, g, b = pixels[x, z]
                block_id = get_closest_block((r, g, b))

                # Calculate brightness (0-1)
                brightness = (r + g + b) / (3 * 255)

                col_height = int(base_height + (brightness * max_height))

                # Create column
                for y in range(col_height):
                    # We can fill the inside with stone or same block
                    # Let's use the colored block for the top layer, and maybe stone below?
                    # Or just solid color. User said "mountain range", usually surface matters.
                    # But "pixel art" suggests solid color.
                    # Let's make it solid color for now as it's simpler and looks like the image from top.
                    blk = Block(block_id, pos=(x, y, z))
                    m.add(blk)

        return m
