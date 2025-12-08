import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from rrs.dsl.parser import RRSParser
from rrs.dsl.ast import Program, ModuleDef, FunctionCall, ExprStmt

def test_parse_simple_instruction():
    code = """
Piston(pos=(0,0,0))
"""
    parser = RRSParser()
    program = parser.parse(code)
    assert isinstance(program, Program)
    assert len(program.statements) == 1
    stmt = program.statements[0]
    assert isinstance(stmt, ExprStmt)
    assert isinstance(stmt.expr, FunctionCall)
    assert stmt.expr.name == "Piston"

def test_parse_module_def():
    code = """
module MyMod(x):
    Piston(pos=(x,0,0))
"""
    parser = RRSParser()
    program = parser.parse(code)
    assert len(program.statements) == 1
    mod = program.statements[0]
    assert isinstance(mod, ModuleDef)
    assert mod.name == "MyMod"
    assert mod.params == ["x"]
    assert len(mod.body) == 1
    assert isinstance(mod.body[0], ExprStmt)
    assert isinstance(mod.body[0].expr, FunctionCall)

def test_parse_math():
    code = """
Piston(pos=(x+1, y*2, z))
"""
    parser = RRSParser()
    program = parser.parse(code)
    # Just checking it parses without error
    assert program