import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter


def test_assignment():
    code = """
module Main():
    x = 10
    Piston(pos=(x, 0, 0))

Main()
"""
    parser = RRSParser()
    tree = parser.parse(code)
    interpreter = Interpreter()
    result = interpreter.visit(tree)
    
    assert len(result.children) == 1
    piston = result.children[0]
    assert piston.pos == (10, 0, 0)

def test_list_and_loop():
    code = """
module Main():
    for x in [1, 2, 3]:
        Piston(pos=(x, 0, 0))

Main()
"""
    parser = RRSParser()
    tree = parser.parse(code)
    interpreter = Interpreter()
    result = interpreter.visit(tree)
    
    assert len(result.children) == 3
    assert result.children[0].pos == (1, 0, 0)
    assert result.children[1].pos == (2, 0, 0)
    assert result.children[2].pos == (3, 0, 0)

def test_range_loop():
    code = """
module Main():
    for x in range(3):
        Piston(pos=(x, 0, 0))

Main()
"""
    parser = RRSParser()
    tree = parser.parse(code)
    interpreter = Interpreter()
    result = interpreter.visit(tree)
    
    assert len(result.children) == 3
    assert result.children[0].pos == (0, 0, 0)
    assert result.children[1].pos == (1, 0, 0)
    assert result.children[2].pos == (2, 0, 0)

def test_range_start_stop():
    code = """
module Main():
    for x in range(1, 4):
        Piston(pos=(x, 0, 0))

Main()
"""
    parser = RRSParser()
    tree = parser.parse(code)
    interpreter = Interpreter()
    result = interpreter.visit(tree)
    
    assert len(result.children) == 3
    assert result.children[0].pos == (1, 0, 0)
    assert result.children[1].pos == (2, 0, 0)
    assert result.children[2].pos == (3, 0, 0)
