# Research: Core Re-RedScript System

**Feature**: Core Re-RedScript System
**Date**: 2025-12-08

## 1. Litematica Integration

**Decision**: Use `litemapy` library.
**Rationale**: 
- It is the standard Python library for reading/writing `.litematic` files.
- It handles the complex NBT structure and region management required by Litematica.
- It allows manipulation of block data which is essential for RRS.
**Alternatives**:
- *Manual NBT parsing with `nbtlib`*: Too complex and prone to errors; re-inventing the wheel.
- *Other NBT libraries*: `litemapy` is specifically built for this format.

## 2. 3D Visualization

**Decision**: Use `ursina` engine.
**Rationale**:
- Extremely simple API for creating voxel/block-based scenes.
- Built-in `FirstPersonController` allows easy inspection.
- Lightweight enough for a viewer tool.
- Python-native and easy to install via pip.
**Alternatives**:
- *Matplotlib*: Too slow for large numbers of blocks; not interactive enough.
- *Pyglet/OpenGL*: Too low-level; requires writing custom shaders/mesh generation.
- *Open3D*: Focused on point clouds, not voxel grids with textures.

## 3. Module Composition & Assertion

**Decision**: Custom `Module` class with recursive composition + Custom `rrs_assert` function.
**Rationale**:
- Composition: Modules need to store relative positions and calculate absolute positions on flattening/export.
- Assertions: `pytest` is for build-time tests. `rrs_assert` is a runtime feature for the user. It needs to provide specific, readable feedback about *which* block property failed (e.g., "Block at (0,1,0) has id 'stone', expected 'dirt'").
