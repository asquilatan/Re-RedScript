# Implementation Plan: Core Re-RedScript System

**Branch**: `001-rrs-core-system` | **Date**: 2025-12-08 | **Spec**: [specs/001-rrs-core-system/spec.md](../specs/001-rrs-core-system/spec.md)
**Input**: Feature specification from `specs/001-rrs-core-system/spec.md`

## Summary

The Core Re-RedScript System establishes the foundational `Module` class, allowing hierarchical composition of Minecraft blocks with `id`, `pos`, and `size`. It includes a `.litematic` import/export engine to interface with Minecraft, an assertion framework (`rrs_assert`) for validation, and a 3D viewer for previewing structures.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: 
- `litemapy` (for .litematic NBT handling)
- `ursina` (for 3D visualization)
**Storage**: File system (.litematic files)
**Testing**: `pytest`
**Target Platform**: Desktop (Windows/Linux/macOS)
**Project Type**: Python Library
**Performance Goals**: Support structures up to ~10k blocks with instant assertions; Viewer < 5s load time.
**Constraints**: Must run locally; minimal heavy dependencies preferred.
**Scale/Scope**: Core library + CLI tools.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Debugging First**: Plan includes `rrs_assert` as a core priority. (Pass)
- **II. Modular Architecture**: Core design is based on `Module` class. (Pass)
- **III. Module Anatomy**: `Module` defined with `id`, `size`, `pos`. (Pass)
- **IV. Reference Implementation**: Will follow `sample_code.py` patterns. (Pass)
- **V. Composition & Export**: Includes `rrs_export` and hierarchical composition. (Pass)

## Project Structure

### Documentation (this feature)

```text
specs/001-rrs-core-system/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── rrs/
│   ├── __init__.py
│   ├── core/
│   │   ├── module.py
│   │   ├── block.py
│   │   └── assertion.py
│   ├── io/
│   │   ├── exporter.py
│   │   └── importer.py
│   ├── viz/
│   │   └── viewer.py
│   └── utils/
│       └── math.py
tests/
├── unit/
├── integration/
└── assets/
```

**Structure Decision**: Standard Python `src/package` layout.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |