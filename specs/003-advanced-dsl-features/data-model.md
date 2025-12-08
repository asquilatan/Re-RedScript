# Data Model: Advanced DSL

## 1. Abstract Syntax Tree (AST) Extensions

### 1.1 New Structural Nodes
| Node | Description | Properties |
|------|-------------|------------|
| `Assignment` | Variable assignment | `target`: str, `value`: Expr |
| `ForLoop` | Loop structure | `var`: str, `iterable`: Expr, `body`: List[Statement] |
| `FuncDef` | Function definition | `name`: str, `params`: List[str], `body`: List[Statement] |
| `ReturnStmt` | Return value | `value`: Expr |
| `ImportStmt` | Import entire file | `module`: str, `alias`: Optional[str] |
| `FromImportStmt`| Import specific symbols | `module`: str, `names`: List[str] |

### 1.2 New Expression Nodes
| Node | Description | Properties |
|------|-------------|------------|
| `ListExpr` | List literal `[a, b]` | `elements`: List[Expr] |
| `MethodCall` | Object method call | `obj`: str, `method`: str, `args`: List[Arg] |
| `GetAttr` | Attribute access `obj.attr` | `obj`: str, `attr`: str |

## 2. Runtime Entities

### 2.1 Scope Management
- **Global Scope**: Top-level variables and imports of a file.
- **Module Scope**: Variables inside a `module ...:` block.
- **Function Scope**: Variables inside a `def ...:` block.
- **Loop Scope**: (Decision: loops do NOT create a new scope in Python, so we follow that).

### 2.2 Built-in Functions
- `range(start, stop)`: Returns an iterable of numbers.
- `Module()`: Constructor for `rrs.core.module.Module`.

## 3. Validation Rules

- **Import Paths**: Must be relative and exist.
- **Method Calls**: Object must have the method (checked at runtime).
- **Return**: Only valid inside `def` or `module` blocks.
