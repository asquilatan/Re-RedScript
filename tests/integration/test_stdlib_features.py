import os
import json
import pytest
from rrs.dsl.interpreter import Interpreter
from rrs.dsl.parser import RRSParser as Parser
from rrs.core.module import Module
from rrs.core.block import Block

# Fixture to setup a directory with blocks.json
@pytest.fixture
def test_env(tmp_path):
    # Create blocks.json
    blocks_def = {
        "SuperBlock": {
            "id": "mod:super_block",
            "defaults": {
                "power": 10
            }
        }
    }
    blocks_path = tmp_path / "blocks.json"
    with open(blocks_path, "w", encoding="utf-8") as f:
        json.dump(blocks_def, f)
        
    return tmp_path

def test_stdlib_and_custom_blocks(test_env):
    script_content = """
from std import Line, Path, Bezier

module TestMod():
    # 1. Test Custom Block
    sb = SuperBlock(pos=(0, 0, 0))
    add(sb)
    
    # 2. Test StdLib Line
    # Line(start, end, block_type)
    # Line from (0,0,0) to (2,0,0) should produce 3 blocks
    l = Line((0, 1, 0), (2, 1, 0), Stone)
    add(l)
    
    # 3. Test Path
    # Path with smooth=False
    p = Path([(0, 2, 0), (0, 4, 0)], Stone, smooth=False)
    add(p)

tm = TestMod()
export(tm)
"""
    script_path = test_env / "test_script.rrs"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
        
    # Run Interpreter
    # We must pass base_dir=test_env so it finds blocks.json
    interpreter = Interpreter(base_dir=str(test_env))
    parser = Parser()
    
    ast = parser.parse(script_content)
    interpreter.run(ast)
    
    # Check exports
    assert len(interpreter.exports) == 1
    exported_module = interpreter.exports[0]
    
    flattened = exported_module.flatten()
    
    # Analyze blocks
    # 1. SuperBlock at (0,0,0)
    sb_found = False
    for b in flattened:
        if b.pos == (0,0,0):
             assert b.id == "mod:super_block"
             # Check default prop if accessible, currently defaults are merged into kwargs but Block might not store them as attrs unless generic
             # Block stores kwargs. 
             # Let's check getattr logic or internal properties if exposed.
             # Block class stores properties in self.properties usually? 
             # Looking at Block class in core/block.py: 
             # super().__init__(id, pos, size, **kwargs) -> Module stores kwargs as ?
             # Module stores **kwargs as attributes?
             # Let's verify standard Block behavior.
             sb_found = True
    assert sb_found
    
    # 2. Line blocks at (0,1,0), (1,1,0), (2,1,0)
    line_blocks = [b for b in flattened if b.pos[1] == 1]
    assert len(line_blocks) == 3
    for lb in line_blocks:
        assert lb.id == "minecraft:stone"
        
    # 3. Path blocks from (0,2,0) to (0,4,0) -> (0,2,0), (0,3,0), (0,4,0)
    path_blocks = [b for b in flattened if 2 <= b.pos[1] <= 4 and b.pos[0] == 0 and b.pos[2] == 0]
    assert len(path_blocks) == 3
