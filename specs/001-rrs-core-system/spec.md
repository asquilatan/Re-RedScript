# Feature Specification: Core Re-RedScript System

**Feature Branch**: `001-rrs-core-system`
**Created**: 2025-12-08
**Status**: Draft
**Input**: User description: "Read @sample_code.py . The specifications are there. We will be creating Re-redscript, which allows the user to programmatically create buildings in a game called minecraft. Everything will be divided into modules. It also allows the user to export it as a .litematic file, convert .litematic files into objects within the language, view litematic files, and the most importantly assert the properties of modules."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Module Definition & Composition (Priority: P1)

As a Re-RedScript user, I want to define structures as "Modules" with specific properties (id, size, pos) and compose them hierarchically, so that I can programmatically design complex Minecraft buildings.

**Why this priority**: This is the fundamental building block of the language. Without modules, nothing else can exist.

**Independent Test**: Define a `SimpleModule` (e.g., a few blocks) and a `ComplexModule` (containing `SimpleModule`), then inspect their internal structure in memory to verify hierarchy and coordinate offsets.

**Acceptance Scenarios**:
1.  **Given** a Python script importing the RRS library, **When** I define a class/function representing a module with `id`, `size`, and `pos`, **Then** the system recognizes it as a valid module.
2.  **Given** a defined `Piston` module, **When** I instantiate it inside a `Engine` module at a specific offset `(x, y, z)`, **Then** the `Piston`'s absolute position is calculated correctly relative to the `Engine`.

---

### User Story 2 - Litematic Export & Import (Priority: P1)

As a user, I want to export my modules to `.litematic` files and import existing `.litematic` files as modules, so that I can interface with the Minecraft Litematica mod.

**Why this priority**: Essential for the "RedScript" part—interoperability with the actual game.

**Independent Test**: Export a generated module to `test.litematic`, then import `test.litematic` back into a new module variable, and assert that the blocks in the imported module match the original.

**Acceptance Scenarios**:
1.  **Given** a module instance `s`, **When** I call `rrs_export(s, "filename")`, **Then** a valid `.litematic` file is created on disk.
2.  **Given** a `.litematic` file, **When** I call `rrs_import("file.litematic", "MyMod")`, **Then** I get a module object that I can place/compose in other modules.

---

### User Story 3 - Debugging with Assertions (Priority: P2)

As a developer using RRS, I want to assert that modules have specific properties (like position or ID), so that I can debug my build logic and prevent regressions.

**Why this priority**: The user explicitly stated "most importantly assert the properties of modules". Crucial for the "Re-" (Reproducible/Reliable) aspect.

**Independent Test**: Write a failing test case where two blocks differ by position, and verify `rrs_assert` returns `False` (or raises error) with a descriptive message.

**Acceptance Scenarios**:
1.  **Given** two identical block modules at `(0,0,0)`, **When** I call `rrs_assert(b1, b2, "id", "pos")`, **Then** it returns `True`.
2.  **Given** blocks at `(0,0,0)` and `(0,1,0)`, **When** I call `rrs_assert(b1, b2, "pos")`, **Then** it returns `False`.
3.  **Given** a complex structure (list of blocks), **When** I assert it against a "correct_structure" list, **Then** it validates every block in the list.

---

### User Story 4 - 3D Visualization (Priority: P3)

As a user, I want to view my generated module in a 3D viewer window, so that I can visually verify the structure before exporting or building.

**Why this priority**: Visual feedback is important but strict correctness (assertions) is higher priority.

**Independent Test**: Call `rrs_viewer(module)` and verify a window opens displaying the correct blocks.

**Acceptance Scenarios**:
1.  **Given** a module instance, **When** I call `rrs_viewer(module)`, **Then** a graphical window opens rendering the blocks.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: System MUST provide a base `Module` concept where every instance has `id` (string), `size` (tuple/vector), and `pos` (tuple/vector).
-   **FR-002**: System MUST include a standard library of Minecraft blocks (e.g., `Piston`, `Repeater`, `Stone`) with correct default IDs and state properties (e.g., `facing`, `powered`, `delay`).
-   **FR-003**: System MUST support defining modules as functions/classes that instantiate sub-modules (composition), handling coordinate transformations (parent pos + child pos).
-   **FR-004**: System MUST implement `rrs_export(module, name)` to serialize module data into the `.litematic` binary format (NBT based).
-   **FR-005**: System MUST implement `rrs_import(path, name)` to parse `.litematic` files and reconstruct them as RRS Module objects.
-   **FR-006**: System MUST implement `rrs_assert(obj1, obj2, *properties)` to compare one or more properties between two single modules or two lists of modules (structures).
-   **FR-007**: `rrs_assert` MUST support comparing at least `id` and `pos`, and ideally arbitrary properties like `facing` or `delay`.
-   **FR-008**: System MUST implement `rrs_viewer(module)` to render the module in 3D (likely using a simple library like `ursina`, `pyglet`, or similar, or just converting to litematic and launching an external tool if "view" implies that, but "objects within the language" implies an internal viewer). *Assumption: Internal simple viewer preferred.*

### Key Entities

-   **Module**: The abstract base class/structure for all buildable objects.
-   **Block**: A concrete Module representing a single coordinate in Minecraft space (1x1x1).
-   **Structure**: A collection of Blocks/Modules (often just a Module containing many children).

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: **Export Validity**: generated `.litematic` files can be successfully opened in the official Litematica Minecraft mod (or a reference standard parser) without errors.
-   **SC-002**: **Round-Trip Fidelity**: Importing a `.litematic` file and immediately exporting it results in a functionally identical file (ignoring metadata timestamps).
-   **SC-003**: **Assertion Accuracy**: `rrs_assert` correctly identifies mismatches in `id` or `pos` in 100% of test cases (0 false positives, 0 false negatives).
-   **SC-004**: **Composition Depth**: System supports nesting modules at least 3 levels deep (e.g., Building -> Room -> Furniture -> Block) with correct absolute coordinate calculation.