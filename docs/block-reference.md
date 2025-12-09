# Block Reference

This document lists all built-in block types available in Re-RedScript.

## Redstone Components

| Block | Properties | Example |
|-------|------------|---------|
| `Piston` | `facing` | `Piston(pos=(0,0,0), facing="up")` |
| `StickyPiston` | `facing` | `StickyPiston(pos=(0,0,0), facing="down")` |
| `Observer` | `facing` | `Observer(pos=(0,0,0), facing="south")` |
| `Repeater` | `facing`, `delay` | `Repeater(pos=(0,0,0), facing="north", delay=2)` |
| `Comparator` | `facing`, `mode` | `Comparator(pos=(0,0,0), facing="east", mode="compare")` |
| `RedstoneWire` | - | `RedstoneWire(pos=(0,0,0))` |
| `RedstoneTorch` | - | `RedstoneTorch(pos=(0,0,0))` |
| `RedstoneBlock` | - | `RedstoneBlock(pos=(0,0,0))` |
| `RedstoneLamp` | - | `RedstoneLamp(pos=(0,0,0))` |
| `Lever` | `face`, `facing` | `Lever(pos=(0,0,0), face="wall", facing="north")` |
| `StoneButton` | `face`, `facing` | `StoneButton(pos=(0,0,0), face="floor")` |
| `OakButton` | `face`, `facing` | `OakButton(pos=(0,0,0), face="wall")` |
| `StonePressurePlate` | - | `StonePressurePlate(pos=(0,0,0))` |
| `OakPressurePlate` | - | `OakPressurePlate(pos=(0,0,0))` |
| `Target` | - | `Target(pos=(0,0,0))` |
| `NoteBlock` | - | `NoteBlock(pos=(0,0,0))` |
| `Hopper` | `facing` | `Hopper(pos=(0,0,0), facing="down")` |
| `Dropper` | `facing` | `Dropper(pos=(0,0,0), facing="up")` |
| `Dispenser` | `facing` | `Dispenser(pos=(0,0,0), facing="north")` |
| `TNT` | - | `TNT(pos=(0,0,0))` |

## Rails

| Block | Properties | Example |
|-------|------------|---------|
| `Rail` | `shape` | `Rail(pos=(0,0,0))` |
| `PoweredRail` | `shape`, `powered` | `PoweredRail(pos=(0,0,0), powered=True)` |
| `DetectorRail` | `shape` | `DetectorRail(pos=(0,0,0))` |
| `ActivatorRail` | `shape` | `ActivatorRail(pos=(0,0,0))` |

## Building Blocks

| Block | Properties | Example |
|-------|------------|---------|
| `Stone` | - | `Stone(pos=(0,0,0))` |
| `Cobblestone` | - | `Cobblestone(pos=(0,0,0))` |
| `Dirt` | - | `Dirt(pos=(0,0,0))` |
| `GrassBlock` | - | `GrassBlock(pos=(0,0,0))` |
| `Sand` | - | `Sand(pos=(0,0,0))` |
| `RedSand` | - | `RedSand(pos=(0,0,0))` |
| `Gravel` | - | `Gravel(pos=(0,0,0))` |
| `Glass` | - | `Glass(pos=(0,0,0))` |
| `TintedGlass` | - | `TintedGlass(pos=(0,0,0))` |
| `Glowstone` | - | `Glowstone(pos=(0,0,0))` |
| `SeaLantern` | - | `SeaLantern(pos=(0,0,0))` |

## Special Blocks

| Block | Properties | Example |
|-------|------------|---------|
| `SlimeBlock` | - | `SlimeBlock(pos=(0,0,0))` |
| `HoneyBlock` | - | `HoneyBlock(pos=(0,0,0))` |

## Planks

| Block | Example |
|-------|---------|
| `OakPlanks` | `OakPlanks(pos=(0,0,0))` |
| `SprucePlanks` | `SprucePlanks(pos=(0,0,0))` |
| `BirchPlanks` | `BirchPlanks(pos=(0,0,0))` |
| `JunglePlanks` | `JunglePlanks(pos=(0,0,0))` |
| `AcaciaPlanks` | `AcaciaPlanks(pos=(0,0,0))` |
| `DarkOakPlanks` | `DarkOakPlanks(pos=(0,0,0))` |
| `MangrovePlanks` | `MangrovePlanks(pos=(0,0,0))` |
| `CherryPlanks` | `CherryPlanks(pos=(0,0,0))` |
| `BambooPlanks` | `BambooPlanks(pos=(0,0,0))` |

## Concrete (16 colors)

```python
WhiteConcrete(pos=(0,0,0))
OrangeConcrete(pos=(0,0,0))
MagentaConcrete(pos=(0,0,0))
LightBlueConcrete(pos=(0,0,0))
YellowConcrete(pos=(0,0,0))
LimeConcrete(pos=(0,0,0))
PinkConcrete(pos=(0,0,0))
GrayConcrete(pos=(0,0,0))
LightGrayConcrete(pos=(0,0,0))
CyanConcrete(pos=(0,0,0))
PurpleConcrete(pos=(0,0,0))
BlueConcrete(pos=(0,0,0))
BrownConcrete(pos=(0,0,0))
GreenConcrete(pos=(0,0,0))
RedConcrete(pos=(0,0,0))
BlackConcrete(pos=(0,0,0))
```

## Stained Glass (16 colors)

Same color variants as Concrete: `WhiteStainedGlass`, `OrangeStainedGlass`, etc.

## Terracotta (16 colors + plain)

```python
Terracotta(pos=(0,0,0))        # Plain
WhiteTerracotta(pos=(0,0,0))   # Colored variants
```

## Glazed Terracotta (16 colors)

```python
WhiteGlazedTerracotta(pos=(0,0,0), facing="north")
# ... all 16 colors with facing property
```

## Ore Blocks

| Block | Example |
|-------|---------|
| `IronBlock` | `IronBlock(pos=(0,0,0))` |
| `GoldBlock` | `GoldBlock(pos=(0,0,0))` |
| `DiamondBlock` | `DiamondBlock(pos=(0,0,0))` |
| `EmeraldBlock` | `EmeraldBlock(pos=(0,0,0))` |
| `LapisBlock` | `LapisBlock(pos=(0,0,0))` |

## Generic Block Constructor

For any Minecraft block not listed above:

```python
Block("minecraft:netherite_block", pos=(0,0,0))
Block("minecraft:end_stone", pos=(0,0,0))
Block("minecraft:ancient_debris", pos=(0,0,0))
```

## Common Block Properties

| Property | Values | Description |
|----------|--------|-------------|
| `pos` | `(x, y, z)` | Block position (required) |
| `facing` | `"north"`, `"south"`, `"east"`, `"west"`, `"up"`, `"down"` | Direction the block faces |
| `axis` | `"x"`, `"y"`, `"z"` | Orientation axis (logs, pillars) |
| `delay` | `1`, `2`, `3`, `4` | Repeater delay in ticks |
| `mode` | `"compare"`, `"subtract"` | Comparator mode |
| `powered` | `True`, `False` | Power state |
| `extended` | `True`, `False` | Piston extension state |
| `face` | `"floor"`, `"wall"`, `"ceiling"` | Button/lever attachment |
