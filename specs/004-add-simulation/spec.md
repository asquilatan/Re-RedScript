# Feature Specification: Add simulation functionalities

**Feature Branch**: `004-add-simulation`
**Created**: 2025-12-09
**Status**: Draft
**Input**: User description: "I want to add simulation functionalities..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Redstone Simulation (Priority: P1)

As a developer, I want to simulate basic Redstone interactions (like an observer triggering a piston) so that I can verify my module's logic without opening the game.

**Why this priority**: This is the core functionality requested. Without the ability to simulate basic component interactions, the feature provides no value.

**Independent Test**: Can be fully tested by creating a script with an observer facing a block and a piston, running `Simulate()`, and verifying the piston extends.

**Acceptance Scenarios**:

1. **Given** a module with an observer facing a solid block and a piston adjacent to that block, **When** the observer is triggered (via `Trigger` or `ChangeState`), **Then** the piston should extend after the appropriate tick delay (2 GT pulse from observer).
2. **Given** a simulation running for 10 ticks, **When** `Simulate(m, 10)` is called, **Then** the simulation stops exactly after 10 gameticks.

---

### User Story 2 - Simulation Assertions (Priority: P1)

As a developer, I want to assert the state of blocks within a simulation against a "correct" reference module so that I can automatically validate complex contraptions (like a piston door).

**Why this priority**: Assertions allow for automated testing of RRS scripts, which is a major use case for simulation.

**Independent Test**: Create a test case where a module is simulated and compared against a defined `CorrectModule`.

**Acceptance Scenarios**:

1. **Given** a module `m` and a correct module `cm`, **When** `assert(m, cm, "pos")` is called within a `Simulate` block, **Then** the simulation should verify that blocks in `m` match `cm` at the specified positions.
2. **Given** an assertion fails inside `Simulate`, **When** the `Simulate` call is not assigned to a variable, **Then** the program should terminate with an assertion error.
3. **Given** an assertion fails inside `Simulate`, **When** `result = Simulate(...)` is used, **Then** `result` should be `False` (or contain failure info) and the program continues.

---

### User Story 3 - Infinite Simulation & Asynchronous Updates (Priority: P2)

As a developer, I want the simulation to handle asynchronous updates (quasi-connectivity, redstone propagation) and run indefinitely if needed, so that I can model continuous behaviors or complex timing.

**Why this priority**: Redstone logic is inherently asynchronous and tick-based. Supporting this is essential for accuracy, even if infinite loops are "ill-advised" but intentional.

**Independent Test**: Simulate a clock circuit that runs forever until interrupted, or a complex update chain.

**Acceptance Scenarios**:

1. **Given** a redstone line with repeaters, **When** powered, **Then** the signal should propagate with correct delays (ticks) down the line.
2. **Given** a `Simulate` call with no tick limit, **When** executed, **Then** it should run indefinitely (until manually stopped or internal break).
3. **Given** a module property change, **Then** a block update should be triggered 1 block away to support Quasi-Connectivity.

### Edge Cases

- **Circular Dependencies**: What happens if two observers observe each other? The system should handle the update loop correctly (likely toggling every tick or burnout logic if implemented, otherwise infinite oscillation).
- **Invalid Block States**: What if `ChangeState` sets a property that doesn't exist for a block? The system should likely raise a comprehensive error.
- **Concurrent Updates**: Two sources powering the same block in the same tick. The standard update order (or priority) should be defined or consistent.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement a `Simulate(module, ticks=None)` function.
    - If `ticks` is provided, run for that many gameticks.
    - If `ticks` is None, run indefinitely.
- **FR-002**: System MUST implement `Trigger(module)` and `ChangeState(block, property, value)` to initiate events.
- **FR-003**: The simulation MUST use "Gameticks" (GT) as the base time unit (1 Redstone Tick = 2 GT).
- **FR-004**: System MUST support Redstone component logic, specifically:
    - **Observer**: Emits a 2 GT pulse when triggered.
    - **Piston**: Extends/retracts based on power and pushes blocks (directional logic).
    - **Redstone Dust/Rails**: Transmit power to adjacent blocks.
- **FR-005**: System MUST implement a Block Update system where:
    - Changing a block state triggers updates in adjacent blocks.
    - Updates propagate asynchronously (queued/scheduled by tick).
    - Quasi-connectivity updates (1 block away) are supported.
- **FR-006**: System MUST support assertions within the simulation scope:
    - `assert(m, cm, "pos")`: Check block positions/types against a reference.
    - Support asserting specific lists of blocks (e.g., `m[b1, b2]`).
- **FR-007**: System MUST handle `Simulate` return values:
    - Unassigned call + Assert Fail -> Terminate program.
    - Unassigned call + Assert Pass -> Continue program.
    - Assigned call (`x = Simulate(...)`) -> Return `True/False` (or modified module) without termination on assert fail.
- **FR-008**: The implementation MUST NOT break existing `.rrs` file import/export functionality.

### Key Entities

- **SimulationEngine**: Manages the tick loop and event queue.
- **UpdateQueue**: Stores pending block updates scheduled for future ticks.
- **BlockState**: Represents the dynamic state of a block during simulation (powered, facing, extended, etc.).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A script defining a 2x2 piston door can be simulated, triggered, and asserted against a "closed" state module successfully.
- **SC-002**: Simulation of a simple observer-piston chain results in the piston extending exactly 2 GTs after the observer triggers (or strictly following the defined delay).
- **SC-003**: Existing integration tests for import/export pass 100% with the new simulation code in the codebase.
- **SC-004**: Simulation correctly identifies a mismatch in assertion (e.g., piston failed to extend) and terminates or returns false as per the call style.