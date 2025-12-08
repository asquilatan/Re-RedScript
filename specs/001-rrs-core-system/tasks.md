# Tasks: Core Re-RedScript System

**Input**: Design documents from `/specs/001-rrs-core-system/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/api-signatures.md

**Tests**: Tests are included as per the implementation plan strategy (Contract/Integration tests for key features).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure (src/rrs/core, src/rrs/io, src/rrs/utils, tests/)
- [ ] T002 Initialize Python project with requirements.txt (including litemapy, pytest)
- [ ] T003 [P] Configure linting (flake8/ruff) and formatting (black) tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create base package init file in src/rrs/__init__.py
- [ ] T005 Implement vector/math utility helpers in src/rrs/utils/math.py
- [ ] T006 [P] Create empty scaffolding for Module class in src/rrs/core/module.py
- [ ] T007 [P] Create empty scaffolding for Block class in src/rrs/core/block.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Module Definition & Composition (Priority: P1)

**Goal**: Define structure hierarchy, relative positioning, and coordinate calculation.

**Independent Test**: Define a parent module with children and verify absolute positions of children are correct after flattening.

### Tests for User Story 1
- [ ] T008 [P] [US1] Unit test for Module attributes and composition in tests/unit/test_module.py
- [ ] T009 [P] [US1] Unit test for recursive coordinate flattening in tests/unit/test_flattening.py

### Implementation for User Story 1
- [ ] T010 [US1] Implement Module class `__init__`, `add`, and property storage in src/rrs/core/module.py
- [ ] T011 [US1] Implement Block class (extending Module) with fixed size in src/rrs/core/block.py
- [ ] T012 [US1] Implement `flatten()` method in Module to calculate absolute positions in src/rrs/core/module.py
- [ ] T013 [US1] Define standard Minecraft blocks library (Piston, Repeater, etc.) in src/rrs/core/block.py

**Checkpoint**: Users can create in-memory module trees.

---

## Phase 4: User Story 2 - Litematic Export & Import (Priority: P1)

**Goal**: Interface with Minecraft Litematica mod via .litematic files.

**Independent Test**: Round-trip test: Export a module -> Import it -> Assert equality.

### Tests for User Story 2
- [ ] T014 [P] [US2] Integration test for rrs_export (generate valid file) in tests/integration/test_io.py
- [ ] T015 [P] [US2] Integration test for rrs_import (read file back) in tests/integration/test_io.py

### Implementation for User Story 2
- [ ] T016 [P] [US2] Implement `rrs_export` using litemapy in src/rrs/io/exporter.py
- [ ] T017 [P] [US2] Implement `rrs_import` using litemapy in src/rrs/io/importer.py
- [ ] T018 [US2] Expose export/import functions in top-level src/rrs/__init__.py

**Checkpoint**: Users can save/load their creations to disk.

---

## Phase 5: User Story 3 - Debugging with Assertions (Priority: P2)

**Goal**: Runtime validation of module properties for debugging.

**Independent Test**: `rrs_assert` returns True for matching modules and False (or raises error) for mismatches.

### Tests for User Story 3
- [ ] T019 [P] [US3] Unit test for `rrs_assert` (various property mismatches) in tests/unit/test_assertion.py

### Implementation for User Story 3
- [ ] T020 [US3] Implement `rrs_assert` logic for single Module comparison in src/rrs/core/assertion.py
- [ ] T021 [US3] Extend `rrs_assert` to handle lists of Modules (structures) in src/rrs/core/assertion.py
- [ ] T022 [US3] Expose `rrs_assert` in top-level src/rrs/__init__.py

**Checkpoint**: Debugging tools are available.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T023 [P] Add docstrings and type hints to all core classes
- [ ] T024 Validate quickstart.md example works against implemented code
- [ ] T025 Cleanup temporary test artifacts (exported .litematic files)

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup & Foundational**: Must be done first.
- **US1 (Module)**: Must be done before US2 (IO) because IO needs the Module structure.
- **US2 (IO)**: Can be done after US1.
- **US3 (Assertions)**: Can be done in parallel with US2, as it only depends on US1 (Module).

### User Story Dependencies
- **US1** -> **US2** (Export needs Module)
- **US1** -> **US3** (Assertion needs Module)

### Parallel Opportunities
- T014/T015 (IO Tests) and T019 (Assertion Tests) can be written while T010-T013 (Module Impl) are finishing.
- T016/T017 (IO Impl) and T020/T021 (Assertion Impl) can be done in parallel by different developers.

---

## Implementation Strategy

### MVP First (US1 + US2)
1. Complete Setup + Foundational.
2. Implement Module system (US1) - essential for representing data.
3. Implement IO (US2) - essential for the "RedScript" value (using it in game).
4. Validate with real Litematica mod.

### Incremental Delivery
1. Foundation + US1 -> Library that can build in-memory structures.
2. + US2 -> Library that can produce files.
3. + US3 -> Library with debugging tools.
