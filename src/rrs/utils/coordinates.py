"""Coordinate helpers used by the simulation engine.

These helpers intentionally mirror the Vec3 utilities in
:mod:`rrs.utils.math` but keep simulation-specific concepts
(e.g. neighbor offsets) in a separate module.
"""

from __future__ import annotations

from typing import Iterable, List, Tuple

Vec3 = Tuple[int, int, int]

# Basic facing offsets used by behaviours and the simulation engine
_FACING_OFFSETS = {
    "north": (0, 0, -1),
    "south": (0, 0, 1),
    "west": (-1, 0, 0),
    "east": (1, 0, 0),
    "up": (0, 1, 0),
    "down": (0, -1, 0),
}


def facing_offset(facing: str) -> Vec3:
    """Return a direction vector for a cardinal ``facing`` string.

    Unknown facings default to ``north``.
    """

    return _FACING_OFFSETS.get(facing, _FACING_OFFSETS["north"])


def neighbors(pos: Vec3) -> List[Vec3]:
    """Return the 6 axis-aligned neighbor positions for ``pos``.

    This is sufficient for the initial simulation stories; more complex
    connectivity (e.g. quasi-connectivity) is layered on later.
    """

    x, y, z = pos
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


def offset(pos: Vec3, delta: Vec3) -> Vec3:
    """Apply a delta vector to a position."""
    dx, dy, dz = delta
    x, y, z = pos
    return (x + dx, y + dy, z + dz)


def path(start: Vec3, deltas: Iterable[Vec3]) -> List[Vec3]:
    """Build a list of positions by walking from ``start`` using ``deltas``."""
    out: List[Vec3] = []
    current = start
    for d in deltas:
        current = offset(current, d)
        out.append(current)
    return out


def is_adjacent(a: Vec3, b: Vec3) -> bool:
    """Return True if ``b`` is orthogonally adjacent to ``a`` (6-neighborhood)."""
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]
    return abs(dx) + abs(dy) + abs(dz) == 1


def is_quasi_neighbor(piston_pos: Vec3, source_pos: Vec3) -> bool:
    """Return True if ``source_pos`` powers ``piston_pos`` via quasi-connectivity.

    This models the common Minecraft rule where pistons can be powered by
    blocks one block above and one to the side.
    """
    dx = source_pos[0] - piston_pos[0]
    dy = source_pos[1] - piston_pos[1]
    dz = source_pos[2] - piston_pos[2]
    return (dy == 1) and ((abs(dx) == 1 and dz == 0) or (abs(dz) == 1 and dx == 0))


# Alias for neighbors
get_neighbors = neighbors
