
import os
import pytest
import numpy as np
from PIL import Image
from rrs.stdlib.img import ConvertPicture
from rrs.core.module import Module

@pytest.fixture
def test_image(tmp_path):
    img_path = tmp_path / "test_img.png"
    # Create a small gradient image
    w, h = 10, 10
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            arr[y, x] = [x * 255 // w, y * 255 // h, 128]
    img = Image.fromarray(arr)
    img.save(img_path)
    return str(img_path)

def test_convert_picture_optimization(test_image):
    """
    Verifies that ConvertPicture works correctly after optimization.
    The optimization removes pixel_sum_sq from the distance calculation.
    We check that it produces a Module with blocks.
    """

    module = ConvertPicture(test_image)

    # Check if module is created
    assert isinstance(module, Module)
    assert module.id == "Picture"

    # Check if blocks are populated
    # The output is a Module containing blocks as children
    assert len(module.children) == 100 # 10x10 image

    # Check a specific block color logic (approximate)
    # Pixel (0,0) -> RGB (0, 0, 128)
    # Closest block should be blue-ish.
    # Looking at palette in stdlib/palette.py:
    # minecraft:blue_concrete: (44, 46, 143)
    # minecraft:blue_wool: (53, 57, 157)
    # Distance to concrete: 44^2 + 46^2 + (143-128)^2 = 1936 + 2116 + 225 = 4277
    # Distance to wool: 53^2 + 57^2 + (157-128)^2 = 2809 + 3249 + 841 = 6899
    # Likely blue_concrete or similar.

    # Let's just assert it picked *something* reasonable and didn't crash.
    # We can check specific ID if we trust the deterministic palette.

    b0 = module.children[0]
    # In flat horizontal mode (default):
    # Image (0,0) -> Module (0, 0, 0)
    assert b0.pos == (0, 0, 0)
    assert "blue" in b0.id or "cyan" in b0.id or "purple" in b0.id or "lapis" in b0.id

    # Check another pixel (9, 9) -> RGB (229, 229, 128)
    # Close to white/yellow/sand
    b_last = module.children[-1]
    # Image (9,9) -> Module (9, 0, 9)
    assert b_last.pos == (9, 0, 9)
