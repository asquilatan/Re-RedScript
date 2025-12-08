import pytest
import os
import textwrap
from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter

@pytest.fixture
def setup_modules(tmp_path):
    # Create a module 'utils.rrs'
    utils_code = textwrap.dedent("""
    def add(a, b):
        return a + b
        
    PI = 3.14
    """)
    utils_file = tmp_path / "utils.rrs"
    utils_file.write_text(utils_code)
    
    # Create a module 'math_lib.rrs'
    math_code = textwrap.dedent("""
    def square(n):
        return n * n
    """)
    math_file = tmp_path / "math_lib.rrs"
    math_file.write_text(math_code)
    
    return tmp_path

def test_import_stmt(setup_modules, monkeypatch):
    monkeypatch.chdir(setup_modules)
    
    code = textwrap.dedent("""
    import utils
    
    res = utils.add(10, 20)
    pi_val = utils.PI
    """)
    
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    interpreter.run(program)
    
    assert interpreter.globals.get("res") == 30
    assert interpreter.globals.get("pi_val") == 3.14

def test_from_import_stmt(setup_modules, monkeypatch):
    monkeypatch.chdir(setup_modules)
    
    code = textwrap.dedent("""
    from utils import add, PI
    
    res = add(5, 5)
    """)
    
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    interpreter.run(program)
    
    assert interpreter.globals.get("res") == 10
    assert interpreter.globals.get("PI") == 3.14

def test_import_alias(setup_modules, monkeypatch):
    monkeypatch.chdir(setup_modules)
    
    code = textwrap.dedent("""
    import utils as u
    
    res = u.add(1, 2)
    """)
    
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    interpreter.run(program)
    
    assert interpreter.globals.get("res") == 3

def test_import_cache(setup_modules, monkeypatch, capsys):
    monkeypatch.chdir(setup_modules)
    
    # Create a module that prints when run
    (setup_modules / "side_effect.rrs").write_text('print("Loaded")\n')
    
    code = textwrap.dedent("""
    import side_effect
    import side_effect
    """)
    
    parser = RRSParser()
    program = parser.parse(code)
    interpreter = Interpreter()
    
    interpreter.run(program)
    
    # Should only be loaded once
    captured = capsys.readouterr()
    # Note: captured.out includes our debug prints too
    assert captured.out.count("Loaded") == 1
