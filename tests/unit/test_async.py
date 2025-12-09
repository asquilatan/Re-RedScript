import pytest

from rrs.core.block import Observer, Piston
from rrs.core.module import Module
from rrs.core.simulation import SimulationEngine


def _observer_piston_module():
    m = Module("obs_piston_async")
    obs = Observer(pos=(0, 0, 0), facing="east")
    piston = Piston(pos=(1, 0, 0), facing="east")
    m.add(obs)
    m.add(piston)
    return m, obs, piston


def test_observer_pulse_respects_tick_limit():
    module, obs, piston = _observer_piston_module()

    # Observer facing east watches block at x=-1 (west of observer)
    watched_pos = (-1, 0, 0)

    # With max_ticks=0 the observer's one-tick-later pulse should not fire
    engine = SimulationEngine(module, ticks=0)
    engine.notify_neighbors(watched_pos)
    engine.run()

    piston_block = engine.get_block(piston.pos)
    assert piston_block is not None
    assert piston_block.properties.get("extended") is not True

    # With a higher tick budget the piston should extend
    engine2 = SimulationEngine(module, ticks=5)
    engine2.notify_neighbors(watched_pos)
    engine2.run()

    piston_block2 = engine2.get_block(piston.pos)
    assert piston_block2 is not None
    assert piston_block2.properties.get("extended") is True
