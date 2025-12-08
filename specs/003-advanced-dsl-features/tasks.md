# Tasks: Advanced DSL Features & CLI Tools

## 1. Setup Phase
**Goal**: Prepare the DSL package for new AST nodes and dependencies.
**Files**: `src/rrs/dsl/ast.py`, `src/rrs/dsl/rrs.lark`

- [x] T001 Define new AST nodes in `src/rrs/dsl/ast.py` (Assignment, ForLoop, FuncDef, etc.)
- [x] T002 Update grammar in `src/rrs/dsl/rrs.lark` to include new statements and expressions (lists, methods)
- [x] T003 Update `RRSTransformer` in `src/rrs/dsl/parser.py` to handle new grammar rules
- [x] T004 [P] Create `tests/dsl/test_parser_advanced.py` to verify AST generation for new syntax

## 2. User Story 1: Loops and Variables
**Goal**: Enable variable assignment, lists, and for-loops.
**Files**: `src/rrs/dsl/interpreter.py`

- [x] T005 [US1] Implement `Assignment` handling in Interpreter (update SymbolTable)
- [x] T006 [US1] Implement `ListExpr` evaluation and `List` runtime support
- [x] T007 [US1] Implement `ForLoop` handling in Interpreter (iterate over lists/ranges)
- [x] T008 [US1] Implement `range()` builtin function in Interpreter
- [x] T009 [US1] Create `tests/dsl/test_loops.py` to verify loop execution and variable state

## 3. User Story 2: Functions and Imports
**Goal**: Enable defining/calling functions and importing other files.
**Files**: `src/rrs/dsl/interpreter.py`

- [x] T010 [US2] Implement `FuncDef` handling (store function in SymbolTable)
- [x] T011 [US2] Update `visit_function_call` to handle user-defined functions
- [x] T012 [US2] Implement `ImportStmt` and `FromImportStmt` handling (recursive interpretation)
- [x] T013 [US2] Implement Import Cache to prevent cycles and redundant loading
- [x] T014 [US2] Create `tests/dsl/test_functions.py` to verify function calls and return values
- [x] T015 [US2] Create `tests/dsl/test_imports.py` with multi-file scenarios

## 4. User Story 3: Explicit Module Management
**Goal**: Allow manual `Module` instantiation and `.add()` method calls.
**Files**: `src/rrs/dsl/interpreter.py`

- [x] T016 [US3] Expose `Module` constructor in Interpreter globals
- [x] T017 [US3] Implement `MethodCall` handling in Interpreter (obj.method())
- [x] T018 [US3] Implement `GetAttr` handling in Interpreter (obj.attr)
- [x] T019 [US3] Implement `+=` operator for Module (add child)
- [x] T020 [US3] Implement `ReturnStmt` handling inside `module` blocks to override return value
- [x] T021 [US3] Create `tests/dsl/test_explicit_module.py` to verify manual module construction

## 5. User Story 4: Converting Litematic to RRS
**Goal**: Implement the `rrs convert` CLI command.
**Files**: `src/rrs/io/converter.py`, `src/rrs/cli.py`

- [ ] T022 [US4] Implement `LitematicConverter` class in `src/rrs/io/converter.py` using `litemapy`
- [ ] T023 [US4] Add `convert` subcommand to `src/rrs/cli.py`
- [ ] T024 [US4] Implement logic to iterate litematic regions and generate `Piston(...)` calls
- [ ] T025 [US4] Create `tests/io/test_converter.py` to verify round-trip (compile -> convert -> compile)

## 6. Polish Phase
**Goal**: Final cleanup and edge case handling.

- [ ] T026 Add error handling for circular imports (detect recursion depth)
- [ ] T027 Add error handling for variable shadowing/scope issues
- [ ] T028 Ensure comments are correctly ignored by parser (grammar check)
- [ ] T029 Update docstrings for all new Interpreter methods

## Dependencies

- Phase 1 (Parser) blocks all US phases.
- US1 (Variables) is prerequisite for US2 and US3.
- US2 (Functions) and US3 (Explicit Module) can be done in parallel.
- US4 (Converter) is independent of DSL runtime changes, but depends on valid syntax output.

## Implementation Strategy
1. **Parser Update**: Get the grammar working first (T001-T004).
2. **Runtime Core**: Variables & Loops (T005-T009).
3. **Modularity**: Functions & Imports (T010-T015).
4. **Advanced**: Explicit Module & Methods (T016-T021).
5. **Tooling**: Converter (T022-T025).
