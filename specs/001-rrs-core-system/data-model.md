# Data Model: Core Re-RedScript System

## Entities

### Module
The base unit of construction.
- **id** (string): Unique identifier for the module type/name (e.g., "minecraft:piston" or "MyComplexHouse").
- **pos** (tuple[int, int, int]): Position relative to the parent container. Default `(0, 0, 0)`.
- **size** (tuple[int, int, int]): Bounding box size. Default `(1, 1, 1)`.
- **children** (list[Module]): List of sub-modules contained within this module.
- **properties** (dict): Arbitrary key-value pairs for block states (e.g., `facing`, `powered`).

### Block (extends Module)
Represents a single Minecraft block.
- **id**: Minecraft namespaced ID (e.g., `minecraft:stone`).
- **size**: Always `(1, 1, 1)`.
- **children**: Always empty.
- **properties**: Valid block states for that block type.

## Relationships

- **Composition**: A `Module` can contain multiple `Module`s (1-to-many).
- **Inheritance**: `Block` is a specialized `Module`.

## State Transitions
- **Instantiation**: Created in memory.
- **Flattening**: Recursive resolution of all children's absolute positions (pos + parent.pos).
- **Export**: Serialization of flattened structure to `.litematic`.
