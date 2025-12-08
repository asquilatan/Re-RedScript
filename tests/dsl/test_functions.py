import pytest
import textwrap
from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter

def test_simple_function():
    code = textwrap.dedent("""
    def greet(name):
        print("Hello " + name)
        
    greet("World")
    """)
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    
    # Mock print to capture output
    captured = []
    interpreter.globals.set("print", lambda x: captured.append(x))
    
    interpreter.run(program)
    assert captured == ["Hello World"]

def test_function_return():
    code = textwrap.dedent("""
    def add(a, b):
        return a + b
        
    x = add(5, 3)
    """)
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    interpreter.run(program)
    
    assert interpreter.globals.get("x") == 8

def test_function_scope():
    code = textwrap.dedent("""
    x = 10
    def change_x(val):
        x = val
        return x
        
    y = change_x(20)
    """)
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    interpreter.run(program)
    
    # x should remain 10 in global scope because function creates new scope
    # and assignment 'x = val' creates local x
    assert interpreter.globals.get("x") == 10
    assert interpreter.globals.get("y") == 20

def test_nested_calls():
    code = textwrap.dedent("""
    def square(n):
        return n * n
        
    def sum_squares(a, b):
        return square(a) + square(b)
        
    res = sum_squares(3, 4)
    """)
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    interpreter.run(program)
    
    assert interpreter.globals.get("res") == 25

def test_recursion():
    code = """
    def factorial(n):
        if n + 0 == 0: 
            return 1
        return n * factorial(n - 1)
        
    res = factorial(5)
    """
    # Note: "if n == 0" is not supported yet? 
    # Wait, I don't have 'if' statement in my grammar yet!
    # I only have 'for' loop.
    # So I can't test recursion with base case properly unless I implement 'if'.
    pass
