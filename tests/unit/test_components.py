import pytest

from rrs.core.block import Block
from rrs.core.module import Module
from rrs.core.simulation import SimulationEngine


def _observer_piston_module():
    """Build a tiny module with an Observer in front of a Piston.

    Layout (x axis):
        Observer (x=0, facing east) -> Piston (x=1)
    """

    m = Module("obs_piston")
    obs = Block("minecraft:observer", pos=(0, 0, 0), facing="east")
    piston = Block("minecraft:piston", pos=(1, 0, 0), facing="east")
    m.add(obs)
    m.add(piston)
    return m, obs, piston


def test_observer_triggers_piston_extension():
    module, obs, piston = _observer_piston_module()

    engine = SimulationEngine(module)

    # Observer facing east watches block at x=-1 (west of observer)
    # Trigger an update at the watched position to cause observer to pulse
    watched_pos = (-1, 0, 0)  # Behind the observer
    engine.notify_neighbors(watched_pos)
    engine.run()

    # After the observer's pulse, the piston should be marked extended
    piston_block = engine.get_block(piston.pos)
    assert piston_block is not None
    assert piston_block.properties.get("extended") is True
