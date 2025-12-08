# API Signatures: Core Re-RedScript System

This document defines the public Python API surface for the library.

## Core Module API

```python
class Module:
    def __init__(self, id: str, pos: tuple[int, int, int] = (0, 0, 0), size: tuple[int, int, int] = (1, 1, 1), **kwargs):
        """
        Initialize a generic module.
        :param id: Identifier (e.g. 'minecraft:stone' or 'MyModule')
        :param pos: Relative (x, y, z) tuple
        :param size: (width, height, length) tuple
        :param kwargs: Additional properties (e.g. block states)
        """
        pass

    def add(self, module: 'Module'):
        """Add a child module to this module."""
        pass

    def flatten(self) -> list['Module']:
        """
        recursively calculate absolute positions of all primitive blocks.
        Returns a list of Block objects with absolute coordinates.
        """
        pass

class Block(Module):
    def __init__(self, id: str, pos: tuple[int, int, int] = (0, 0, 0), **properties):
        """
        Initialize a single block. Size is fixed to (1, 1, 1).
        :param properties: Block states like facing='north', powered=True
        """
        pass
```

## IO & Tools API

```python
def rrs_export(module: Module, filename: str) -> None:
    """
    Export a module (and its hierarchy) to a .litematic file.
    :param module: The root module to export
    :param filename: Output path (without extension, or with)
    """
    pass

def rrs_import(path: str, name: str) -> Module:
    """
    Import a .litematic file as a Module.
    :param path: Path to the .litematic file
    :param name: ID to assign to the imported module
    :return: A Module instance containing the blocks from the file
    """
    pass

def rrs_assert(obj1: Module | list[Module], obj2: Module | list[Module], *properties: str) -> bool:
    """
    Assert that two modules or structures are identical regarding specific properties.
    :param obj1: First object (Module or list of Modules)
    :param obj2: Second object (expected)
    :param properties: List of property names to check (e.g. "id", "pos", "facing")
    :return: True if they match, raises AssertionError or returns False otherwise (TBD by implementation preference, spec implies boolean return but 'assert' implies exception). 
             *Spec Clarification*: Spec says "returns True/False".
    """
    pass

def rrs_viewer(module: Module) -> None:
    """
    Open a 3D window to visualize the module.
    :param module: The module to render
    """
    pass
```
