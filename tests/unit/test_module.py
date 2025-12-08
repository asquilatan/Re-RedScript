import pytest
from rrs.core.module import Module

def test_module_initialization():
    m = Module(id="test_module", pos=(1, 2, 3), size=(4, 5, 6))
    assert m.id == "test_module"
    assert m.pos == (1, 2, 3)
    assert m.size == (4, 5, 6)
    assert m.children == []
    assert m.properties == {}

def test_module_defaults():
    m = Module(id="default_module")
    assert m.pos == (0, 0, 0)
    assert m.size == (1, 1, 1)

def test_module_composition():
    parent = Module(id="parent")
    child = Module(id="child")
    parent.add(child)
    assert child in parent.children
    assert len(parent.children) == 1
