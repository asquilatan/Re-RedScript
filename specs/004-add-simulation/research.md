# Research: Add simulation functionalities

## Unknowns & Clarifications

1.  **Simulation State vs Data Model**: Should `Block` objects store runtime state (e.g., "last_powered_tick")?
    *   **Decision**: No.
    *   **Rationale**: `Block` classes in `core` should remain declarative data containers (representing the static structure). Runtime state should be managed by the `SimulationEngine` or a wrapper class (e.g., `SimulatedBlock`) during the simulation lifecycle. This allows a `Module` to be reused or simulated multiple times without state pollution.

2.  **Event Loop Implementation**: How to handle asynchronous updates?
    *   **Decision**: Priority Queue based Event Loop.
    *   **Rationale**: Redstone updates rely on specific timing (ticks) and update order. A priority queue `(scheduled_tick, priority, action)` ensures events happen in the correct order.

3.  **Behavior Logic Location**: Where does the logic for "Observer checks adjacent" live?
    *   **Decision**: `src/rrs/core/behaviors.py`.
    *   **Rationale**: Decouples logic from data. `Block` classes just define *what* they are. `Behaviors` define *how* they act. The `SimulationEngine` looks up the behavior for a block type.

## Technology Choices

-   **Priority Queue**: Python's `heapq` module. Efficient for scheduling events.
-   **Coordinates**: Tuples `(x, y, z)`. Simple and hashable (for dict keys).

## Best Practices (Redstone Simulation)

-   **Quasi-Connectivity**: Pistons/Droppers/Dispensers can be powered by blocks 1 block above + 1 to the side (diagonalish). The simulation needs to check for this specifically.
-   **Update Order**: In Minecraft, update order can be directional or hash-based. For this simulation, we will enforce a consistent deterministic order (e.g., coordinate sorted) to avoid "locational" randomness unless specifically desired.
-   **Pulse Length**: Observers emit 2 GT pulses. Stone buttons 10 GT (wait, spec says 10 redstone ticks usually, but we stick to spec requirement: Observer = 2 GT).

## Alternatives Considered

-   **Modifying `Block` class**: Adding `update()` methods directly to `Block`.
    *   *Rejected*: Bloats the core data model. Makes serialization/deserialization messier if runtime state leaks in.

-   **External Library**: Using a Python Minecraft simulation library (e.g., `mcpy`).
    *   *Rejected*: Too heavy, likely incompatible with our custom DSL/Module structure, and we only need basic logic for now.
