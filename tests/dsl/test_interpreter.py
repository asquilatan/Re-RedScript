import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter
from rrs.core.module import Module
from rrs.core.block import Piston

def test_interpreter_simple():
    code = """
module MyMod(x):
    Piston(pos=(x,0,0))

MyMod(10)
"""
    parser = RRSParser()
    program = parser.parse(code)
    
    interpreter = Interpreter()
    results = interpreter.run(program)
    
    assert len(results) == 1
    mod = results[0]
    assert isinstance(mod, Module)
    assert mod.id == "MyMod"
    
    # Check children
    # Module stores children in self.children list? 
    # Let's check rrs.core.module.Module implementation
    assert len(mod.children) == 1
    child = mod.children[0]
    assert isinstance(child, Piston)
    assert child.pos == (10, 0, 0)

def test_interpreter_nested():
    code = """
module Sub(y):
    Piston(pos=(0,y,0))

module Main(z):
    Sub(z)
    Sub(z+1)

Main(5)
"""
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    results = interpreter.run(program)
    
    assert len(results) == 1
    main = results[0]
    assert main.id == "Main"
    assert len(main.children) == 2
    
    sub1 = main.children[0]
    assert sub1.id == "Sub"
    # Sub1 should have a Piston at (0, 5, 0)
    assert len(sub1.children) == 1
    assert sub1.children[0].pos == (0, 5, 0)
    
    sub2 = main.children[1]
    # Sub2 should have a Piston at (0, 6, 0)
    assert sub2.children[0].pos == (0, 6, 0)