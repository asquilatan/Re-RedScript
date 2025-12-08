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


def test_circular_import_detection(tmp_path, monkeypatch):
    (tmp_path / "a.rrs").write_text("import b\n", encoding="utf-8")
    (tmp_path / "b.rrs").write_text("import a\n", encoding="utf-8")

    code = "import a\n"
    parser = RRSParser()
    tree = parser.parse(code)
    interpreter = Interpreter()

    monkeypatch.chdir(tmp_path)

    with pytest.raises(ImportError, match="Circular import"):
        interpreter.visit(tree)
