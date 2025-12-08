import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from rrs.dsl.parser import RRSParser
from rrs.dsl.ast import (
    Program, ModuleDef, FuncDef, ForLoop, Assignment,
    ImportStmt, FromImportStmt, ReturnStmt, ListExpr,
    MethodCall, GetAttr, FunctionCall, Literal, Variable, ExprStmt
)

def test_parse_assignment():
    code = "x = 1\n"
    parser = RRSParser()
    program = parser.parse(code)
    assert len(program.statements) == 1
    stmt = program.statements[0]
    assert isinstance(stmt, Assignment)
    assert stmt.target == "x"
    assert isinstance(stmt.value, Literal)
    assert stmt.value.value == 1

def test_parse_list():
    code = "x = [1, 2, 3]\n"
    parser = RRSParser()
    program = parser.parse(code)
    stmt = program.statements[0]
    assert isinstance(stmt.value, ListExpr)
    assert len(stmt.value.elements) == 3

def test_parse_for_loop():
    code = """
for x in [1, 2]:
    print(x)
"""
    parser = RRSParser()
    program = parser.parse(code)
    stmt = program.statements[0]
    assert isinstance(stmt, ForLoop)
    assert stmt.target == "x"
    assert isinstance(stmt.iterable, ListExpr)
    assert len(stmt.body) == 1
    assert isinstance(stmt.body[0], ExprStmt)
    assert isinstance(stmt.body[0].expr, FunctionCall)

def test_parse_func_def():
    code = """
def my_func(a, b):
    return a + b
"""
    parser = RRSParser()
    program = parser.parse(code)
    stmt = program.statements[0]
    assert isinstance(stmt, FuncDef)
    assert stmt.name == "my_func"
    assert stmt.params == ["a", "b"]
    assert len(stmt.body) == 1
    assert isinstance(stmt.body[0], ReturnStmt)

def test_parse_imports():
    code = """
import math
from utils import helper, other
"""
    parser = RRSParser()
    program = parser.parse(code)
    assert isinstance(program.statements[0], ImportStmt)
    assert program.statements[0].module_name == "math"
    
    assert isinstance(program.statements[1], FromImportStmt)
    assert program.statements[1].module_name == "utils"
    assert program.statements[1].names == ["helper", "other"]

def test_parse_method_call():
    code = "obj.method(1)\n"
    parser = RRSParser()
    program = parser.parse(code)
    # instruction -> ExprStmt -> method_call
    stmt = program.statements[0]
    assert isinstance(stmt, ExprStmt)
    assert isinstance(stmt.expr, MethodCall)
    call = stmt.expr
    assert isinstance(call.obj, Variable)
    assert call.obj.name == "obj"
    assert call.method == "method"
    assert len(call.args) == 1

def test_parse_getattr():
    code = "x = obj.attr\n"
    parser = RRSParser()
    program = parser.parse(code)
    stmt = program.statements[0]
    assert isinstance(stmt.value, GetAttr)
    assert stmt.value.attr == "attr"
