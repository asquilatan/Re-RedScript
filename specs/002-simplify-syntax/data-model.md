# Data Model: RRS DSL

## 1. Abstract Syntax Tree (AST) Nodes

The DSL parser will produce a tree where nodes represent language constructs.

### 1.1 Structural Nodes
| Node | Description | Properties |
|------|-------------|------------|
| `Program` | Root of the file | `statements`: List[Statement] |
| `ModuleDef` | A module definition | `name`: str, `params`: List[str], `body`: List[Statement] |
| `BlockInst` | A block instantiation | `name`: str, `args`: List[Arg], `kwargs`: List[Kwarg] |
| `ModuleInst` | A module usage | `name`: str, `args`: List[Arg], `kwargs`: List[Kwarg] |

### 1.2 Expression Nodes
| Node | Description | Properties |
|------|-------------|------------|
| `Literal` | Static value | `value`: (int, float, str, bool) |
| `Variable` | Reference to param | `name`: str |
| `BinaryOp` | Math operation | `left`: Expr, `op`: (+, -, *, /), `right`: Expr |
| `TupleExpr` | Coordinates `(x,y,z)` | `elements`: List[Expr] |

## 2. Runtime Entities

These entities exist during the interpretation phase.

### 2.1 Symbol Table
- **ScopeStack**: A stack of dictionaries to handle variable scope (global vs module-local).
- **ModuleRegistry**: Stores `ModuleDef` AST nodes by name to allow lazy instantiation.

### 2.2 Core Mapping
| DSL Entity | Python Core Class | Notes |
|------------|-------------------|-------|
| `module X` | `rrs.core.module.Module` | Instantiated via `Interpreter` |
| `Piston(...)` | `rrs.core.block.Block` | Instantiated and added to parent |

## 3. Validation Rules

- **Parameter Count**: Arguments provided to Module instantiation must match definition.
- **Variable Resolution**: Variables used in expressions must be in scope (defined in Module params).
- **Type Checking**: `pos` argument must evaluate to a 3-tuple of integers.
