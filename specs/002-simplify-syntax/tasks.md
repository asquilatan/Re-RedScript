# Tasks: Simplify RRS Syntax (RRS-DSL)

## 1. Setup Phase
**Goal**: Initialize project structure and dependencies for the DSL.
**Files**: `requirements.txt`, `src/rrs/dsl/__init__.py`, `tests/dsl/__init__.py`

- [x] T001 Install `lark` dependency and add to requirements.txt
- [x] T002 Create DSL package structure `src/rrs/dsl/` with `__init__.py`
- [x] T003 Create DSL tests package structure `tests/dsl/` with `__init__.py`

## 2. Foundational Phase
**Goal**: Implement the core grammar and AST definitions required by all user stories.
**Files**: `src/rrs/dsl/ast.py`, `src/rrs/dsl/parser.py`, `specs/002-simplify-syntax/contracts/rrs.lark`

- [x] T004 Define AST Node classes in `src/rrs/dsl/ast.py` (ModuleDef, BlockInst, Literal, etc.)
- [x] T005 [P] Copy grammar file to `src/rrs/dsl/rrs.lark` (runtime location)
- [x] T006 Implement `RRSParser` class in `src/rrs/dsl/parser.py` using Lark
- [x] T007 [P] Create parser tests in `tests/dsl/test_parser.py` to verify AST generation for basic module syntax

## 3. User Story 1: Defining a Simple Module
**Goal**: Allow users to define a module with basic blocks like Piston and Repeater.
**Files**: `src/rrs/dsl/interpreter.py`, `src/rrs/cli.py`

- [x] T008 [US1] Implement `Interpreter` class skeleton in `src/rrs/dsl/interpreter.py` with SymbolTable
- [x] T009 [US1] Implement `ModuleDef` handling in Interpreter (registering modules)
- [x] T010 [US1] Implement `BlockInst` handling in Interpreter (instantiating `rrs.core.Block`)
- [x] T011 [US1] Create `tests/dsl/test_interpreter.py` to verify module registration and block addition
- [x] T012 [US1] Implement CLI command `rrs compile` in `src/rrs/cli.py` to accept `.rrs` file

## 4. User Story 2: Exporting a Structure
**Goal**: Compile the interpreted module to a `.litematic` file.
**Files**: `src/rrs/cli.py`, `src/rrs/dsl/interpreter.py`

- [x] T013 [US2] Update Interpreter to return a compiled `Module` object
- [x] T014 [US2] Connect CLI `compile` command to `rrs_export` in `src/rrs/io/exporter.py`
- [x] T015 [US2] Create integration test `tests/dsl/test_cli_export.py` verifying file creation

## 5. User Story 3: Nested Modules & Math
**Goal**: Support module nesting and arithmetic expressions in arguments.
**Files**: `src/rrs/dsl/interpreter.py`

- [x] T016 [US3] Implement `ModuleInst` handling in Interpreter (calling other modules)
- [x] T017 [US3] Implement expression evaluation in Interpreter (Math, Variables, Tuples)
- [x] T018 [US3] Implement ScopeStack in Interpreter to handle parameters (x, y, z)
- [x] T019 [US3] Add nested module tests in `tests/dsl/test_interpreter.py`

## 6. User Story 4: Edge Cases
**Goal**: Handle invalid syntax, undefined references, and circular dependencies.
**Files**: `src/rrs/dsl/parser.py`, `src/rrs/dsl/interpreter.py`

- [x] T020 [US4] Add error handling in Parser for syntax errors (re-raise with line info)
- [x] T021 [US4] Add validation in Interpreter for undefined modules/blocks
- [x] T022 [US4] Add recursion detection in Interpreter (circular module calls)
- [x] T023 [US4] Add edge case tests in `tests/dsl/test_errors.py`

## 7. Polish Phase
**Goal**: Final cleanup and documentation.

- [x] T024 Add docstrings to all DSL classes
- [x] T025 Review and update quickstart guide if syntax changed
- [x] T026 Ensure all tests pass with `pytest`

## Dependencies

- Phase 1 & 2 must be complete before any US phase.
- US1 is prerequisite for US2 and US3.
- US2 and US3 can be done in parallel after US1.
- US4 is best done last or iteratively.

## Implementation Strategy
1. **MVP**: T001-T012 (Setup + Parser + Simple Interpreter) -> Can run `Scenario 1`.
2. **Export**: T013-T015 -> Can produce files.
3. **Full Features**: T016-T019 -> Nesting and Math.
4. **Robustness**: T020-T023 -> Error handling.
