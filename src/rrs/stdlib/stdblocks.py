import os
from rrs.core.block import load_blocks_from_json, Block
from typing import Dict, Type

def get_standard_blocks() -> Dict[str, Type[Block]]:
    """Loads Standard Library blocks from blocks.json in this directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "blocks.json")
    return load_blocks_from_json(json_path)
