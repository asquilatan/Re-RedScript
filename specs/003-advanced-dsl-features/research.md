# Research: Advanced DSL Features

## 1. Unknowns & Clarifications

### 1.1 Grammar Expansion
**Question**: How to extend the existing Lark grammar to support imperative features (assignments, loops, imports) without breaking backward compatibility?
- **Decision**: Add new statement types to the `statement` rule.
- **Rules to Add**:
    - `assignment`: `CNAME EQUALS expression`
    - `for_loop`: `FOR CNAME IN expression COLON suite`
    - `func_def`: `DEF CNAME LPAR [params] RPAR COLON suite`
    - `import_stmt`: `IMPORT ...` / `FROM ... IMPORT ...`
    - `return_stmt`: `RETURN expression`
- **Rationale**: Lark's EBNF is flexible. We can simply expand the `statement` disjunction.

### 1.2 Import Mechanism
**Question**: How to implement imports in the interpreter?
- **Decision**:
    1. Parse the import path (relative to current file).
    2. Check a `loaded_modules` cache to prevent cycles/redundant parsing.
    3. If new, spawn a recursive `Interpreter` instance to run that file.
    4. Extract the desired symbols (or the whole global scope) and merge into the current `SymbolTable`.
- **Alternatives**: Python's `importlib` (would require transpiling RRS to Python, which we rejected in 002).

### 1.3 Module Instantiation & Methods
**Question**: How to support `module.add()`?
- **Decision**:
    - The `Module` class in `rrs.core.module` already has `.add()`.
    - We need to expose this method to the DSL interpreter.
    - `FunctionCall` logic needs to distinguish between "Calling a DSL Module/Function" and "Calling a Method on an Object".
    - **New AST Node**: `MethodCall` (e.g., `obj.method(args)`).

## 2. Technology Selection

- **Parser**: Continue using `lark` (proven in Feature 002).
- **Litematic Reading**: `litemapy` (already in requirements.txt).

## 3. Best Practices

- **Scoping**: Implement a robust `ScopeStack` where creating a function/module pushes a new scope, and looking up a variable traverses up the stack.
- **Recursion Limits**: Enforce a max import depth to prevent crashes from circular imports if detection fails.
