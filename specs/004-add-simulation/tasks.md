# Tasks: Add simulation functionalities

**Feature Branch**: `004-add-simulation`
**Spec**: [specs/004-add-simulation/spec.md](spec.md)

## Implementation Strategy

We will implement the simulation engine in layers:
1.  **Core Data Structures**: `SimulatedBlock`, `Event`, and the `SimulationEngine` skeleton.
2.  **Basic Simulation Loop**: Implementing the tick loop and event processing.
3.  **Behaviors**: Implementing `Observer` and `Piston` behaviors (US1).
4.  **DSL Integration**: Exposing `Simulate` and `Trigger` to the language (US1).
5.  **Assertions**: Adding the testing capabilities (US2).
6.  **Advanced Logic**: Asynchronous updates and Quasi-Connectivity (US3).

## Dependencies

- **US1** (Basic Sim) depends on **Foundation**.
- **US2** (Assertions) depends on **US1**.
- **US3** (Async) depends on **US1**.

## Phase 1: Setup

- [X] T001 Create `src/rrs/core/simulation.py` with empty class definitions
- [X] T002 Create `src/rrs/core/behaviors.py` with empty class definitions
- [X] T003 Create `src/rrs/utils/coordinates.py` for coordinate math helpers
- [X] T004 Use existing `tests/unit` package for simulation tests (no separate `tests/simulation` directory)

## Phase 2: Foundational (Engine Core)

**Goal**: Establish the data structures and event loop mechanics required for any simulation.

- [X] T005 [P] Implement `SimulatedBlock` class in `src/rrs/core/simulation.py` (properties, position)
- [X] T006 [P] Implement `Event` class in `src/rrs/core/simulation.py` (priority, callback, args)
- [X] T007 [P] Implement `BlockBehavior` base interface in `src/rrs/core/behaviors.py`
- [X] T008 Implement `SimulationEngine.__init__` in `src/rrs/core/simulation.py` (load module into world dict)
- [X] T009 Implement `SimulationEngine.schedule` and priority queue management in `src/rrs/core/simulation.py`
- [X] T010 Implement `SimulationEngine.run` tick loop structure (process events per tick) in `src/rrs/core/simulation.py`

## Phase 3: User Story 1 - Basic Redstone Simulation

**Goal**: Simulate basic Redstone interactions (Observer -> Piston) to verify module logic.
**Independent Test**: `test_components.py` simulating an Observer triggering a Piston.

- [X] T011 [P] [US1] Create `tests/unit/test_components.py` with failing test for Observer-Piston interaction
- [X] T012 [P] [US1] Implement `ObserverBehavior` in `src/rrs/core/behaviors.py` (emit pulse on update)
- [X] T013 [P] [US1] Implement `PistonBehavior` in `src/rrs/core/behaviors.py` (extend/retract logic)
- [X] T014 [US1] Implement `SimulationEngine.trigger_update` to notify behaviors of neighbor changes in `src/rrs/core/simulation.py`
- [X] T015 [US1] Implement `Interpreter.func_Trigger` and `func_ChangeState` in `src/rrs/dsl/interpreter.py`
- [X] T016 [US1] Implement `Interpreter.func_Simulate` to run `SimulationEngine` in `src/rrs/dsl/interpreter.py`
- [X] T017 [US1] Register `Simulate`, `Trigger`, `ChangeState` built-ins in `src/rrs/dsl/interpreter.py`

## Phase 4: User Story 2 - Simulation Assertions

**Goal**: Assert state of blocks within a simulation against a "correct" reference.
**Independent Test**: `test_assertions.py` verifying pass/fail scenarios.

- [X] T018 [P] [US2] Create `tests/unit/test_assertions.py`
- [X] T019 [US2] Implement `assert_module_state` helper function in `src/rrs/core/simulation.py` (compare world vs module)
- [X] T020 [US2] Implement `assert` keyword/function logic within `Interpreter` context during simulation in `src/rrs/dsl/interpreter.py`
- [X] T021 [US2] Update `Interpreter.func_Simulate` to handle return values (bool vs termination) based on assertions in `src/rrs/dsl/interpreter.py`

## Phase 5: User Story 3 - Infinite Simulation & Async

**Goal**: Handle asynchronous updates and infinite loops for continuous logic.
**Independent Test**: `test_async.py` checking update propagation.

- [X] T022 [P] [US3] Create `tests/unit/test_async.py`
- [X] T023 [US3] Refine `SimulationEngine.trigger_update` to queue updates asynchronously (next tick or later in current tick) in `src/rrs/core/simulation.py`
- [X] T024 [US3] Implement Quasi-Connectivity check logic (e.g., check block above-diagonal) in `src/rrs/core/behaviors.py` (Pistons)
- [X] T025 [US3] Ensure `SimulationEngine.run` handles `ticks=None` correctly (infinite loop) in `src/rrs/core/simulation.py`

## Phase 6: Polish

- [X] T026 Run full test suite (`pytest`) to ensure no regressions in import/export
- [X] T027 Verify error messages for invalid block states or assertion failures are clear
