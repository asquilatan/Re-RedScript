## 2025-02-18 - [Optimizing Hollow Cuboid Generation]
**Learning:** Generating hollow 3D shapes by iterating the full volume and checking `is_border` is extremely inefficient ((N^3)$). Explicitly iterating over the 2D surfaces ((N^2)$) provides massive speedups (measured ~2.6x for 100x100x100, theoretically much higher for larger shapes).
**Action:** When generating hollow geometric primitives, always iterate the surface coordinates directly rather than filtering volume coordinates.
