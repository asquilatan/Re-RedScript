import pytest

from rrs.core.block import Stone
from rrs.core.module import Module
from rrs.core.simulation import SimulationEngine, assert_module_state


def _make_modules_matching():
    actual = Module("actual")
    expected = Module("expected")

    actual.add(Stone(pos=(0, 0, 0)))
    expected.add(Stone(pos=(0, 0, 0)))
    return actual, expected


def test_assert_module_state_passes_for_matching_world():
    actual, expected = _make_modules_matching()

    engine = SimulationEngine(actual)
    # No events – world should mirror the original module
    assert assert_module_state(engine, expected, "id") is True


def test_assert_module_state_raises_for_mismatch():
    actual, expected = _make_modules_matching()

    # Move the expected block
    expected.children[0].pos = (1, 0, 0)

    engine = SimulationEngine(actual)

    with pytest.raises(AssertionError):
        assert_module_state(engine, expected, "id")
