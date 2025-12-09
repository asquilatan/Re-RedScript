# Data Model: Add simulation functionalities

## Core Entities

### SimulationEngine
The central controller for the simulation.

- **Fields**:
    - `world`: `Dict[Tuple[int, int, int], SimulatedBlock]` - The state of the world.
    - `event_queue`: `List[Event]` - Priority queue of scheduled events.
    - `current_tick`: `int` - Current gametick (starts at 0).
    - `max_ticks`: `Optional[int]` - Limit for simulation.

### SimulatedBlock
Represents the runtime state of a block.

- **Fields**:
    - `block_type`: `Type[Block]` - The class of the block (e.g., `Observer`).
    - `properties`: `Dict[str, Any]` - Current state properties (e.g., `{"facing": "north", "powered": True}`).
    - `position`: `Tuple[int, int, int]` - Coordinate in the simulation.

### Behavior (Interface)
Defines how a block type acts.

- **Methods**:
    - `on_tick(sim: SimulationEngine, block: SimulatedBlock)`: Called every tick (or when scheduled).
    - `on_update(sim: SimulationEngine, block: SimulatedBlock, source_pos: Tuple[int, int, int])`: Called when a neighbor changes.
    - `on_place(sim: SimulationEngine, block: SimulatedBlock)`: Called when initialized.
    - `on_interact(sim: SimulationEngine, block: SimulatedBlock, action: str)`: Called by `Trigger`.

### Event
A scheduled action in the queue.

- **Fields**:
    - `tick`: `int` - When it should execute.
    - `priority`: `int` - Order within the same tick (lower = earlier).
    - `callback`: `Callable` - The function to run.
    - `args`: `Tuple` - Arguments for the callback.

## Relationships

- `SimulationEngine` *contains* many `SimulatedBlock`s.
- `SimulationEngine` *uses* `Behavior`s to update `SimulatedBlock`s.
- `Interpreter` *creates* and *runs* `SimulationEngine`.
