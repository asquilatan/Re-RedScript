from typing import Tuple

Vec3 = Tuple[int, int, int]

def add_vec3(v1: Vec3, v2: Vec3) -> Vec3:
    """Add two 3D vectors (tuples)."""
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])

def sub_vec3(v1: Vec3, v2: Vec3) -> Vec3:
    """Subtract v2 from v1."""
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])
