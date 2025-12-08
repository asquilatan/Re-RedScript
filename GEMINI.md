# Re-RedScript (RRS) Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-08

## Active Technologies
- Python 3.10+ + `lark` (Parsing) (002-simplify-syntax)
- File System (`.rrs` input, `.litematic` output) (002-simplify-syntax)
- Python 3.10+ + `lark` (Parsing), `litemapy` (Litematic I/O) (003-advanced-dsl-features)
- File System (`.rrs`, `.litematic`) (003-advanced-dsl-features)

- Python 3.10+ (001-rrs-core-system)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.10+: Follow standard conventions

## Recent Changes
- 003-advanced-dsl-features: Added Python 3.10+ + `lark` (Parsing), `litemapy` (Litematic I/O)
- 002-simplify-syntax: Implemented the Re-RedScript (RRS) Domain Specific Language (DSL) parser, interpreter, and command-line interface (CLI) for compiling `.rrs` files to `.litematic`. This includes support for module definitions, block instantiations, and arithmetic expressions.

**Note on `rrs` command**: To execute `rrs` directly from the command line, you must install the project in editable mode using `pip install -e .` from the project root. Alternatively, you can run it via `python -m rrs.cli compile <file.rrs>` after setting `PYTHONPATH=src`.

- 001-rrs-core-system: Added Python 3.10+

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
