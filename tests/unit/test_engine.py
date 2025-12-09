import pytest

from rrs.core.block import Block
from rrs.core.module import Module
from rrs.core.simulation import SimulationEngine, SimulatedBlock


def _make_simple_module():
    m = Module("test", pos=(0, 0, 0))
    m.add(Block("minecraft:stone", pos=(1, 2, 3)))
    return m


def test_engine_initializes_world_from_module():
    m = _make_simple_module()
    engine = SimulationEngine(m)

    # World should contain a simulated block at the same position
    pos = (1, 2, 3)
    sb = engine.get_block(pos)
    assert isinstance(sb, SimulatedBlock)
    assert sb.position == pos
    assert sb.id == "minecraft:stone"


def test_engine_runs_scheduled_events_in_order():
    m = _make_simple_module()
    engine = SimulationEngine(m)

    events = []

    def cb(name):
        events.append((engine.current_tick, name))

    # Same tick, different priority
    engine.schedule(1, 10, cb, "late")
    engine.schedule(1, 0, cb, "early")

    # Later tick
    engine.schedule(3, 5, cb, "later")

    engine.run()

    assert events == [
        (1, "early"),
        (1, "late"),
        (3, "later"),
    ]
