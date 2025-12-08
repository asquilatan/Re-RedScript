# Quickstart: Writing RRS Scripts

This guide explains how to use the new `.rrs` syntax to define Minecraft structures.

## 1. Basic Structure

An `.rrs` file consists of module definitions. A module is a reusable component.

```python
# Define a module named 'MyPiston' taking 3 coordinates
module MyPiston(x, y, z):
    # Instantiate blocks inside. They are automatically added to the module.
    Piston(pos=(x, y, z), facing="up")
    Stone(pos=(x, y-1, z))
```

## 2. Instantiation

You can use modules you've defined, or built-in blocks.

```python
module Main(x, y, z):
    # Use the module defined above
    MyPiston(x, y, z)
    
    # Use it again offset by 2 blocks
    MyPiston(x+2, y, z)
```

## 3. Compiling

To convert your script to a `.litematic` file:

```bash
rrs compile input.rrs --output output.litematic
```

## 4. Syntax Reference

- **Definition**: `module Name(args):` followed by an indented block.
- **Calls**: `Name(arg1, key=val)`.
- **Math**: Basic arithmetic `+ - * /` is supported in arguments.
- **Tuples**: `(1, 2, 3)` are used for coordinates.
