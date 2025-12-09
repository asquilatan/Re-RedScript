"""Core simulation engine for RRS.

Initial skeleton; behavior and DSL integration are implemented in later tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import heapq
import copy

from rrs.core.module import Module
from rrs.core.block import Block
from rrs.core.assertion import rrs_assert


Position = Tuple[int, int, int]


@dataclass(order=True)
class Event:
    tick: int
    priority: int
    callback: Callable[..., Any] = field(compare=False, repr=False)
    _counter: int = field(default=0, compare=True, repr=False)
    args: Tuple[Any, ...] = field(default_factory=tuple, compare=False, repr=False)


@dataclass
class SimulatedBlock:
    block_type: type
    properties: Dict[str, Any]
    position: Position


def _world_to_module(world: Dict[Position, "SimulatedBlock"]) -> Module:
    """Convert the internal world dict back into a :class:`Module`.

    The helper is intentionally tiny and only used for assertion-style
    checks where a flat structure is sufficient.
    """
    module = Module("world")
    for pos, sblock in world.items():
        block = sblock.block_type(pos=pos, **sblock.properties)
        module.add(block)
    return module


def assert_module_state(engine: "SimulationEngine", expected: Module, *properties: str, **kwargs: Any) -> bool:
    """Compare the engine's world against an expected module.

    This is a light wrapper over :func:`rrs.core.assertion.rrs_assert` so
    that simulation tests can remain decoupled from the internal
    representation of ``world``.
    """
    actual = _world_to_module(engine.world)
    return rrs_assert(actual, expected, *properties, **kwargs)


class SimulationEngine:
    """Skeleton for the Redstone simulation engine.

    Concrete behavior is added in later tasks; for now only basic
    structure and storage fields are defined.
    """

    def __init__(self, module: Module, ticks: Optional[int] = None) -> None:
        """Initializes the simulation with a module.

        The constructor flattens the given :class:`Module` into a
        ``world`` dictionary keyed by absolute position.
        """
        if not isinstance(module, Module):
            raise TypeError(f"SimulationEngine expects a Module, got {type(module).__name__}")

        self.world: Dict[Position, SimulatedBlock] = {}
        self.event_queue: List[Event] = []
        self.current_tick: int = 0
        self.max_ticks: Optional[int] = ticks
        self._counter: int = 0
        self._source_module: Module = module
        # Power levels (0-15) for each block position
        self.power_levels: Dict[Position, int] = {}

        # Populate the world from the module hierarchy
        for block in module.flatten():
            if not isinstance(block, Block):
                # Only concrete blocks participate in the simulation
                continue
            pos: Position = block.pos  # flatten() already returns absolute positions
            props = copy.deepcopy(block.properties)
            self.world[pos] = SimulatedBlock(block_type=type(block), properties=props, position=pos)

    def run(self) -> None:
        """Runs the simulation loop until ``max_ticks`` or the queue is empty.

        Events are processed in order of increasing ``tick`` and then by
        ``priority`` (lower values first).  After each event the
        ``current_tick`` is advanced to the event's tick.
        """
        while self.event_queue:
            event = heapq.heappop(self.event_queue)

            # Respect an optional max tick bound
            if self.max_ticks is not None and event.tick > self.max_ticks:
                break

            self.current_tick = event.tick
            event.callback(*event.args)

    def schedule(self, delay: int, priority: int, callback: Callable[..., Any], *args: Any) -> None:
        """Schedules an event on the internal priority queue.

        ``delay`` is relative to the current tick; ``priority`` is used
        to order events within the same tick (lower runs first).
        """
        if delay < 0:
            raise ValueError("delay must be non-negative")

        tick = self.current_tick + delay
        self._counter += 1
        event = Event(tick=tick, priority=priority, _counter=self._counter, callback=callback, args=args)
        heapq.heappush(self.event_queue, event)

    def get_block(self, pos: Position) -> Optional[SimulatedBlock]:
        """Returns the block at position."""
        return self.world.get(pos)

    def set_block(self, pos: Position, block: SimulatedBlock) -> None:
        """Sets/Places a block at the given position."""
        self.world[pos] = block

    def trigger_update(self, pos: Position) -> None:
        """Notify the block at ``pos`` that it has been updated.

        The block's registered behaviour is invoked, which can in turn
        schedule further events or notify its neighbors.
        """
        block = self.get_block(pos)
        if block is None:
            return

        # Import lazily to avoid circular imports at module load time
        from rrs.core.behaviors import get_behavior

        behavior = get_behavior(block.block_type)
        if behavior is None:
            return

        behavior.on_neighbor_update(self, pos, pos)

    def notify_neighbors(self, source_pos: Position) -> None:
        """Notify all blocks adjacent to source_pos that it has changed.
        
        This is used when a block at source_pos changes state and neighbors
        (like observers) need to react to the change.
        """
        from rrs.utils.coordinates import neighbors
        from rrs.core.behaviors import get_behavior
        
        for neighbor_pos in neighbors(source_pos):
            block = self.get_block(neighbor_pos)
            if block is None:
                continue
            
            behavior = get_behavior(block.block_type)
            if behavior:
                behavior.on_neighbor_update(self, neighbor_pos, source_pos)

    def change_state(self, block: SimulatedBlock, property_name: str, value: Any) -> None:
        """Change a block's state property and trigger updates.
        
        This is used within simulations to modify block properties like
        'powered', 'extended', etc.
        """
        if block.position not in self.world:
            raise ValueError(f"Block at {block.position} is not in the simulation")
        
        # Update the property
        block.properties[property_name] = value
        
        # Trigger block update for propagation
        self.trigger_update(block.position)
