# Feature Specification: Advanced DSL Features & CLI Tools

## 1. Context and Scope

The initial RRS DSL (Feature 002) provided a basic declarative syntax for defining Minecraft structures. However, complex logic requires imperative programming features—loops, variables, functions, and modular imports—to be truly powerful. Additionally, users need a way to migrate existing `.litematic` files into RRS scripts to edit them.

This feature expands the RRS DSL into a full-fledged scripting language with control flow, variable management, and modularity, while also adding a "decompiler" tool to the CLI.

### Scope
- **DSL Syntax Extension**:
    - Variable assignment (`x = 10`) and list support (`[1, 2]`).
    - Control flow: `for` loops (`range`, iterables).
    - Function definitions (`def name(args): ...`).
    - Module import system (`import`, `from ... import`).
    - Explicit `Module` instantiation and return values within `module` blocks.
    - Comments (`#`).
- **CLI Extension**:
    - `rrs convert <file.litematic>` command to generate `.rrs` source code.
- **Out of Scope**:
    - Full Python compatibility (we are not implementing all of Python, just a subset).
    - Object-Oriented Programming (classes) beyond the built-in `Module` type.

## 2. User Scenarios

### Scenario 1: Using Loops and Variables
**Actor**: RRS Developer
**Action**: Writes a script to generate a staircase.
**Input**:
```python
module Staircase(height):
    for i in range(0, height):
        # Calculate position
        pos_x = i
        pos_y = i
        Stone(pos=(pos_x, pos_y, 0))
```
**Outcome**: The compiler generates a staircase of `height` steps.

### Scenario 2: Importing Libraries
**Actor**: RRS Developer
**Action**: Reuses common logic from another file.
**Input**:
*utils.rrs*:
```python
def get_offset(i):
    return i * 2
```
*main.rrs*:
```python
from utils import get_offset

module Main():
    x = get_offset(5)
    Piston(pos=(x, 0, 0))
```
**Outcome**: `Main` module uses the imported function to determine coordinates.

### Scenario 3: Explicit Module Management
**Actor**: Advanced User
**Action**: Manually constructs a module object for fine-grained control.
**Input**:
```python
module CustomLogic():
    # Create explicit container
    container = Module()
    
    p1 = Piston(pos=(0,0,0))
    container.add(p1)
    
    # Operator overloading requested
    container += Stone(pos=(0,1,0))
    
    return container
```
**Outcome**: The `CustomLogic` module returns the manually constructed `container` instead of an implicitly gathered list of blocks.

### Scenario 4: Converting Litematic to RRS
**Actor**: RRS Developer
**Action**: Converts an existing building to a script.
**Input**: `rrs convert house.litematic -o house.rrs`
**Outcome**: A `house.rrs` file is created containing `module House():` with a long list of block definitions representing the structure.

### Scenario 5: Edge Cases
- **Circular Imports**: `a.rrs` imports `b.rrs` which imports `a.rrs`. System must detect and raise error.
- **Variable Shadowing**: Inner scope variable has same name as outer scope. System should resolve to inner variable (standard scoping).
- **Invalid Litematic**: Converter given a corrupted file. Should exit with clear error message.

## 3. Functional Requirements

### 3.1 Language Features
- **FR1 (Variables)**: Support assignment `var = expr` and usage of variables in expressions.
- **FR2 (Lists)**: Support list literals `[a, b]` and basic indexing/iteration.
- **FR3 (Loops)**: Support `for var in iterable:` syntax. Implement `range(start, stop)` builtin.
- **FR4 (Functions)**: Support `def name(args): body` and `return expr`.
- **FR5 (Imports)**: Support `import filename` (as namespace) and `from filename import symbol`. Paths should be relative to current file.
- **FR6 (Comments)**: Ignore text starting with `#` until newline.

### 3.2 Module Object Features
- **FR7 (Explicit Instantiation)**: Allow `Module()` constructor to create a new empty module.
- **FR8 (Methods)**: Support `.add(child)` method on Module instances.
- **FR9 (Operators)**: Support `+=` operator for adding children to a Module.
- **FR10 (Explicit Return)**: If a `module` block executes a `return` statement, that value represents the module, overriding the implicit behavior.

### 3.3 CLI Tools
- **FR11 (Convert)**: Implement `rrs convert input.litematic` which reads a schematic and writes valid `.rrs` source code.

## 4. Success Criteria

- **SC1**: A script using `for` loops and variables to create a 10x10 grid of blocks compiles correctly.
- **SC2**: A script importing a function from another file executes correctly.
- **SC3**: `rrs convert` successfully transforms a valid `.litematic` file into an `.rrs` file, and running `rrs compile` on that result produces an identical structure (round-trip equality).

## 5. Assumptions & Dependencies

- **Assumption**: `range()` behaves like Python's range (start, exclusive stop).
- **Assumption**: Imports are resolved relative to the executing script's directory.
- **Dependency**: `litemapy` library is required for reading `.litematic` files in the converter.

## 6. Questions & Clarifications

*Resolved: Scoping Rules*
- **Decision**: Option A (Python-like Lexical Scoping).
- **Reasoning**: To minimize user confusion and support robust code reuse, variables defined within functions or modules will be local to that scope.

*Resolved: Convert Format*
- **Decision**: Option A (Raw Dump).
- **Reasoning**: The primary goal is to enable editing of existing structures. A raw list of blocks is guaranteed to be accurate and easy to implement. Pattern recognition is too complex for this phase.