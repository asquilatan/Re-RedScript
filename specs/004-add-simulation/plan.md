# Implementation Plan: Add simulation functionalities

**Branch**: `004-add-simulation` | **Date**: 2025-12-09 | **Spec**: [specs/004-add-simulation/spec.md](spec.md)
**Input**: Feature specification from `specs/004-add-simulation/spec.md`

## Summary

Implement a Redstone simulation engine (`Simulate`, `Trigger`, `ChangeState`) allowing developers to verify module logic (Observer, Piston, Dust) within the RRS DSL, including support for assertions and asynchronous updates, without breaking existing import/export.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `lark` (for parsing)
**Storage**: N/A (in-memory simulation)
**Testing**: `pytest`
**Target Platform**: Windows/Linux/macOS (CLI)
**Project Type**: CLI/Library
**Performance Goals**: N/A (simulation speed is not primary concern yet, correctness is)
**Constraints**: Must not break existing `.rrs` parsing or `.litematic` export.
**Scale/Scope**: Core simulation logic for ~5-10 block types initially (Observer, Piston, Dust, Repeater, Air, Solid Block).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Simple & Idiomatic**: Pythonic class structure for simulation.
- **No Over-Engineering**: Using a simple tick loop and priority queue.
- **Safety**: Simulation runs in a controlled loop (infinite loop protection/warning as per spec).

## Project Structure

### Documentation (this feature)

```text
specs/004-add-simulation/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
├── rrs/
│   ├── core/
│   │   ├── block.py        # Modify (add properties/methods if needed)
│   │   ├── simulation.py   # NEW: SimulationEngine, UpdateQueue
│   │   └── behaviors.py    # NEW: Logic for specific blocks (Observer, Piston, etc.)
│   ├── dsl/
│   │   ├── interpreter.py  # Modify (add Simulate, Trigger, ChangeState builtins)
│   │   └── rrs.lark        # No changes expected unless syntax needs it (unlikely)
│   └── utils/
│       └── coordinates.py  # NEW: Helper for relative coordinate math (optional but likely needed)
└── tests/
    └── unit/               # Existing unit tests + new simulation tests
        ├── test_engine.py
        ├── test_components.py
        ├── test_assertions.py
        └── test_async.py
```

**Structure Decision**: Added `simulation.py` and `behaviors.py` to `core` to house the new logic. Tests added in `tests/simulation`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Separate `behaviors.py` | To keep `Block` class clean and data-focused | Putting logic in `Block` couples data with runtime behavior strongly. |