import os
import sys
import textwrap

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter
from rrs.core.module import Module


def run_script(source: str):
    parser = RRSParser()
    program = parser.parse(textwrap.dedent(source))
    interpreter = Interpreter()
    results = interpreter.run(program)
    return interpreter, results


def test_module_factory_generates_ids():
    code = """
    container = Module()
    """
    interpreter, results = run_script(code)
    assert results == []
    container = interpreter.globals.get("container")
    assert isinstance(container, Module)
    assert container.id.startswith("anon_module_")


def test_module_return_override_with_add():
    code = """
    module Custom():
        container = Module("CustomContainer")
        piston = Piston(pos=(2, 0, 0))
        container.add(piston)
        return container

    Custom()
    """
    _, results = run_script(code)
    assert len(results) == 1
    container = results[0]
    assert container.id == "CustomContainer"
    assert len(container.children) == 1
    child = container.children[0]
    assert child.pos == (2, 0, 0)


def test_module_plus_equal_adds_block():
    code = """
    module Custom():
        container = Module()
        container += Stone(pos=(0, 1, 0))
        return container

    Custom()
    """
    _, results = run_script(code)
    assert len(results) == 1
    container = results[0]
    assert len(container.children) == 1
    stone = container.children[0]
    assert stone.pos == (0, 1, 0)


def test_module_plus_equal_accepts_nested_modules():
    code = """
    module Builder():
        child = Module("Inner")
        child += Stone(pos=(1, 0, 0))
        container = Module("Outer")
        container += child
        return container

    Builder()
    """
    _, results = run_script(code)
    assert len(results) == 1
    outer = results[0]
    assert outer.id == "Outer"
    assert len(outer.children) == 1
    inner = outer.children[0]
    assert inner.id == "Inner"
    assert len(inner.children) == 1
    assert inner.children[0].pos == (1, 0, 0)
