# Research: Simplify RRS Syntax (DSL)

## 1. Unknowns & Clarifications

### 1.1 Parsing Strategy
**Question**: How should we parse the new `.rrs` syntax?
- **Option A**: Manual Recursive Descent Parser. (Good for control, no dependencies. Bad for maintenance).
- **Option B**: `lark` (Modern, fast, EBNF support, standalone).
- **Option C**: `ply` (Classic, verbose).
- **Option D**: `transpilation` to Python (replace `module` with `class` via regex).

**Decision**: **Option B (Lark)**.
**Rationale**:
- Lark is widely used, robust, and allows defining grammar in a separate EBNF file, which is great for documentation and maintainability.
- It produces a parse tree that we can walk to instantiate our existing Python objects.
- Transpilation (Option D) is risky because reporting syntax errors back to the original line numbers is hard, and "regex parsing" is fragile.

### 1.2 Integration with Core
**Question**: How to map DSL to existing `Module` / `Block` classes?
- **Decision**: **Interpreter Pattern**.
- **Mechanism**:
    1. Parse `.rrs` file -> AST (Lark Tree).
    2. Traverse AST.
    3. For `module Definition`: Create a factory/registry entry.
    4. For `Instantiations` (e.g., `Piston(...)`):
        - If inside a module definition: Store as a "recipe" step.
        - If at top level: Instantiate immediately.
    5. The Interpreter maintains a `SymbolTable` (functions, variables).

### 1.3 Arithmetic Expressions
**Question**: The spec requires `pos=(x+1, y, z)`. How to handle expressions?
- **Decision**: Use Lark's expression evaluation capabilities or just Python's `eval` (restricted) if safe, but better to implement a simple expression evaluator visitor to avoid security risks of `eval()`.
- **Refinement**: Since this is a local tool for developers, strict sandboxing isn't the primary concern, but a custom evaluator is cleaner for a DSL. We will implement basic arithmetic nodes in the AST.

## 2. Technology Selection

- **Parser**: `lark` (Python library).
- **Extension**: `.rrs` (Re-RedScript).
- **Output**: `.litematic` (via existing `rrs_export`).

## 3. Best Practices

- **Grammar Separation**: Keep `.lark` grammar file separate from Python code.
- **Error Handling**: Provide friendly error messages pointing to line/column.
- **Testing**: Test grammar with various valid/invalid inputs independently of execution.
