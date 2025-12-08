"""
Re-RedScript (RRS) Core Library
"""

__version__ = "0.1.0"

from rrs.core.module import Module
from rrs.core.block import (
    Block, Stone, Piston, Repeater,
    GoldBlock, DiamondBlock, EmeraldBlock, Glowstone, SeaLantern,
    RedstoneBlock, LapisBlock, IronBlock, Observer
)
from rrs.io.exporter import rrs_export
from rrs.io.importer import rrs_import
from rrs.core.assertion import rrs_assert


