import os
import textwrap
from pathlib import Path

from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter
from rrs.io.converter import LitematicConverter
from rrs.io.exporter import rrs_export


def _flatten_blocks(module):
    blocks = []
    for block in module.flatten():
        props = tuple(sorted(block.properties.items()))
        blocks.append((block.id, block.pos, props))
    blocks.sort()
    return blocks


def _build_sample_module():
    code = textwrap.dedent(
        """
        module Sample():
            Stone(pos=(0, 0, 0))
            Block("minecraft:oak_log", pos=(1, 0, 0), axis="x")
        
        s = Sample()
        export(s)
        """
    )
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    modules = interpreter.run(program)
    return modules[0]


def test_converter_round_trip(tmp_path):
    module = _build_sample_module()
    litematic_path = tmp_path / "sample.litematic"
    rrs_export(module, str(litematic_path))

    converter = LitematicConverter()
    output_path = tmp_path / "converted.rrs"
    converter.convert(str(litematic_path), str(output_path), module_name="Converted")

    parser = RRSParser()
    program = parser.parse_file(output_path)
    interpreter = Interpreter()
    rebuilt_modules = interpreter.run(program)
    assert len(rebuilt_modules) == 1

    original_blocks = _flatten_blocks(module)
    rebuilt_blocks = _flatten_blocks(rebuilt_modules[0])
    assert original_blocks == rebuilt_blocks


def test_converter_generates_reasonable_defaults(tmp_path):
    module = _build_sample_module()
    litematic_path = tmp_path / "house schematic.litematic"
    rrs_export(module, str(litematic_path))

    converter = LitematicConverter()
    output_path = converter.convert(str(litematic_path))

    assert os.path.exists(output_path)
    contents = Path(output_path).read_text(encoding="utf-8")
    assert "module HouseSchematic()" in contents
    assert "export(m)" in contents