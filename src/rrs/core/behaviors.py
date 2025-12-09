"""Block behavior definitions for the simulation engine.

This module defines how blocks interact with redstone power and
react to state changes during simulation.
"""

from __future__ import annotations

from typing import Dict, Tuple, TYPE_CHECKING, Type, Optional, List

from rrs.core.block import Block
from rrs.utils.coordinates import facing_offset, is_adjacent, is_quasi_neighbor, get_neighbors

if TYPE_CHECKING:  # pragma: no cover - for type checkers only
    from rrs.core.simulation import SimulationEngine, SimulatedBlock

Position = Tuple[int, int, int]
BlockState = Dict[str, object]


# Simple registry mapping block IDs to their behaviours
_BEHAVIORS: Dict[str, "BlockBehavior"] = {}


def register_behavior(block_id: str, behavior: "BlockBehavior") -> None:
    _BEHAVIORS[block_id] = behavior


def get_behavior(block_id: str) -> Optional["BlockBehavior"]:
    # Check if passed arg is a type/class by mistake, but we expect string ID now.
    if not isinstance(block_id, str):
         # If called with type, try to handle gracefully or assume caller fixed.
         return None
    return _BEHAVIORS.get(block_id)


class BlockBehavior:
    """Base behavior interface for simulated blocks."""

    def on_tick(self, sim: "SimulationEngine", pos: Position, block_state: BlockState) -> None:
        """Called on each tick or when scheduled."""
        pass

    def on_neighbor_update(self, sim: "SimulationEngine", pos: Position, source_pos: Position) -> None:
        """Called when this block is notified that a neighbor was updated."""
        pass

    def on_state_change(self, sim: "SimulationEngine", pos: Position, property_name: str, old_value, new_value) -> None:
        """Called when a block's state property changes."""
        pass

    def get_power_output(self, sim: "SimulationEngine", pos: Position) -> int:
        """Return the power level this block outputs (0-15)."""
        return 0


class LeverBehavior(BlockBehavior):
    """Lever - power source that outputs 15 when powered."""

    def get_power_output(self, sim: "SimulationEngine", pos: Position) -> int:
        block = sim.get_block(pos)
        if block and block.properties.get("powered", False):
            return 15
        return 0

    def on_state_change(self, sim: "SimulationEngine", pos: Position, property_name: str, old_value, new_value) -> None:
        if property_name == "powered":
            # Notify all adjacent blocks
            for neighbor_pos in get_neighbors(pos):
                sim.schedule(0, 1, lambda np=neighbor_pos: sim.trigger_update(np))


class RedstoneBlockBehavior(BlockBehavior):
    """Redstone Block - always outputs power level 15."""

    def get_power_output(self, sim: "SimulationEngine", pos: Position) -> int:
        return 15


class RedstoneWireBehavior(BlockBehavior):
    """Redstone Wire - conducts power with 1 level loss per block."""

    def on_neighbor_update(self, sim: "SimulationEngine", pos: Position, source_pos: Position) -> None:
        block = sim.get_block(pos)
        if block is None:
            return
        
        # Calculate max power from neighbors
        max_power = 0
        for neighbor_pos in get_neighbors(pos):
            neighbor = sim.get_block(neighbor_pos)
            if neighbor:
                behavior = get_behavior(neighbor.id)
                if behavior:
                    power = behavior.get_power_output(sim, neighbor_pos)
                    max_power = max(max_power, power)
        
        # Wire loses 1 power level
        new_power = max(0, max_power - 1)
        old_power = block.properties.get("power", 0)
        
        if new_power != old_power:
            block.properties["power"] = new_power
            sim.power_levels[pos] = new_power
            # Propagate to neighbors
            for neighbor_pos in get_neighbors(pos):
                np = neighbor_pos
                sim.schedule(0, 2, lambda np=np: sim.trigger_update(np))

    def get_power_output(self, sim: "SimulationEngine", pos: Position) -> int:
        block = sim.get_block(pos)
        if block:
            return block.properties.get("power", 0)
        return 0


class RepeaterBehavior(BlockBehavior):
    """Repeater - delays and refreshes power signal."""

    def on_neighbor_update(self, sim: "SimulationEngine", pos: Position, source_pos: Position) -> None:
        block = sim.get_block(pos)
        if block is None:
            return

        facing = str(block.properties.get("facing", "north"))
        delay_ticks = int(block.properties.get("delay", 1)) * 2  # Convert to GT
        
        # Check input (behind the repeater)
        input_offset = facing_offset(facing)
        input_pos = (pos[0] - input_offset[0], pos[1] - input_offset[1], pos[2] - input_offset[2])
        
        input_block = sim.get_block(input_pos)
        powered = False
        if input_block:
            behavior = get_behavior(input_block.id)
            if behavior and behavior.get_power_output(sim, input_pos) > 0:
                powered = True

        def _update_output():
            output_pos = (pos[0] + input_offset[0], pos[1] + input_offset[1], pos[2] + input_offset[2])
            sim.trigger_update(output_pos)

        if powered and not block.properties.get("powered", False):
            block.properties["powered"] = True
            sim.schedule(delay=delay_ticks, priority=0, callback=_update_output)
        elif not powered and block.properties.get("powered", False):
            block.properties["powered"] = False
            sim.schedule(delay=delay_ticks, priority=0, callback=_update_output)

    def get_power_output(self, sim: "SimulationEngine", pos: Position) -> int:
        block = sim.get_block(pos)
        if block and block.properties.get("powered", False):
            return 15
        return 0


class ObserverBehavior(BlockBehavior):
    """Observer - emits 2 GT pulse when detecting block changes."""

    def on_neighbor_update(self, sim: "SimulationEngine", pos: Position, source_pos: Position) -> None:
        block = sim.get_block(pos)
        if block is None:
            return

        # Determine the block being watched (opposite of facing)
        facing = str(block.properties.get("facing", "north"))
        dx, dy, dz = facing_offset(facing)
        watched_pos: Position = (pos[0] - dx, pos[1] - dy, pos[2] - dz)

        # Only react if the watched block changed
        if source_pos != watched_pos:
            return

        # Emit pulse to the block behind us
        output_pos: Position = (pos[0] + dx, pos[1] + dy, pos[2] + dz)

        def _start_pulse():
            block.properties["powered"] = True
            sim.trigger_update(output_pos)

        def _end_pulse():
            block.properties["powered"] = False
            sim.trigger_update(output_pos)

        # 2 GT pulse
        sim.schedule(delay=1, priority=0, callback=_start_pulse)
        sim.schedule(delay=3, priority=0, callback=_end_pulse)

    def get_power_output(self, sim: "SimulationEngine", pos: Position) -> int:
        block = sim.get_block(pos)
        if block and block.properties.get("powered", False):
            return 15
        return 0


class PistonBehavior(BlockBehavior):
    """Piston - extends when powered, with quasi-connectivity support."""

    def on_neighbor_update(self, sim: "SimulationEngine", pos: Position, source_pos: Position) -> None:
        block = sim.get_block(pos)
        if block is None:
            return

        # Check power from adjacent blocks AND quasi-connectivity
        powered = self._is_powered(sim, pos)

        if powered and not block.properties.get("extended", False):
            # Extend after 3 GT (1.5 redstone ticks)
            def _extend():
                block.properties["extended"] = True
            sim.schedule(delay=3, priority=0, callback=_extend)

        elif not powered and block.properties.get("extended", False):
            # Retract after 3 GT
            def _retract():
                block.properties["extended"] = False
            sim.schedule(delay=3, priority=0, callback=_retract)

    def _is_powered(self, sim: "SimulationEngine", pos: Position) -> bool:
        """Check if piston is powered (including quasi-connectivity)."""
        # Check direct neighbors
        for neighbor_pos in get_neighbors(pos):
            neighbor = sim.get_block(neighbor_pos)
            if neighbor:
                behavior = get_behavior(neighbor.id)
                if behavior and behavior.get_power_output(sim, neighbor_pos) > 0:
                    return True

        # Check quasi-connectivity (block above + adjacent to above)
        above_pos = (pos[0], pos[1] + 1, pos[2])
        for neighbor_pos in get_neighbors(above_pos):
            if is_quasi_neighbor(pos, neighbor_pos):
                neighbor = sim.get_block(neighbor_pos)
                if neighbor:
                    behavior = get_behavior(neighbor.id)
                    if behavior and behavior.get_power_output(sim, neighbor_pos) > 0:
                        return True

        return False


class RedstoneLampBehavior(BlockBehavior):
    """Redstone Lamp - lights up when powered."""

    def on_neighbor_update(self, sim: "SimulationEngine", pos: Position, source_pos: Position) -> None:
        block = sim.get_block(pos)
        if block is None:
            return

        powered = False
        for neighbor_pos in get_neighbors(pos):
            neighbor = sim.get_block(neighbor_pos)
            if neighbor:
                behavior = get_behavior(neighbor.id)
                if behavior and behavior.get_power_output(sim, neighbor_pos) > 0:
                    powered = True
                    break

        block.properties["lit"] = powered


# Register default behaviours
# Register default behaviours
register_behavior("minecraft:observer", ObserverBehavior())
register_behavior("minecraft:piston", PistonBehavior())
register_behavior("minecraft:sticky_piston", PistonBehavior())  # Same behavior as regular piston for now
register_behavior("minecraft:lever", LeverBehavior())
register_behavior("minecraft:redstone_block", RedstoneBlockBehavior())
register_behavior("minecraft:redstone_wire", RedstoneWireBehavior())
register_behavior("minecraft:repeater", RepeaterBehavior())
register_behavior("minecraft:redstone_lamp", RedstoneLampBehavior())
