import pytest
from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter

def test_infinite_recursion():
    code = """module A():
    A()

A()
"""
    parser = RRSParser()
    tree = parser.parse(code)
    interpreter = Interpreter()
    
    # This should ideally raise a specific error, but for now let's see if it hits Python's RecursionError
    with pytest.raises(RecursionError):
        interpreter.visit(tree)

def test_undefined_variable():
    code = """module A():
    Piston(pos=(x, 0, 0))

A()
"""
    parser = RRSParser()
    tree = parser.parse(code)
    interpreter = Interpreter()
    
    with pytest.raises(NameError, match="Undefined variable: x"):
        interpreter.visit(tree)

def test_undefined_module():
    code = """module A():
    B()

A()
"""
    parser = RRSParser()
    tree = parser.parse(code)
    interpreter = Interpreter()
    
    with pytest.raises(NameError, match="Unknown block or module: B"):
        interpreter.visit(tree)
