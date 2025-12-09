"""
Re-RedScript (RRS) Core Library
"""

__version__ = "0.1.0"

from rrs.core.module import Module
from rrs.core.block import Block
from rrs.io.exporter import rrs_export
from rrs.io.importer import rrs_import
from rrs.core.assertion import rrs_assert

__all__ = [
    "Module", "rrs_export", "rrs_import", "rrs_assert", "Block"
]
