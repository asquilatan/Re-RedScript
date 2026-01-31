## 2024-05-23 - Block.flatten Optimization
**Learning:** `copy.copy` overhead on simple objects like `Block` is significant (~600ms vs ~140ms for 100k calls). Manually cloning via `__new__` and `__dict__.copy()` yields a ~76% speedup, far exceeding the expected 35%. This suggests that for high-frequency object duplication in this codebase (like during flattening), avoiding standard copy mechanisms is critical.
**Action:** When cloning simple state-container objects in hot paths, prefer `__new__` + `__dict__` copy over `copy.copy`, provided `__slots__` are not used.

## 2026-01-07 - ConvertPicture Optimization
**Learning:** In nearest-neighbor search using Euclidean distance ($||p - q||^2 = ||p||^2 + ||q||^2 - 2 p \cdot q$), the term $||p||^2$ (query pixel energy) is constant for all candidates $. It can be omitted when only the index of the minimum distance (argmin) is required. This avoids one large broadcasting addition and the calculation of pixel sums, yielding a ~20% speedup for image conversion.
**Action:** When implementing nearest-neighbor searches where only the ranking matters, strip out constant terms from the distance metric to reduce operations.

## 2026-01-08 - Cylinder Rasterization Optimization
**Learning:** For extruded 3D shapes (like cylinders), checking geometric conditions (e.g., `dist_sq <= r^2`) for every point in the 3D bounding box is computationally expensive (O(H * R^2)). Pre-calculating the 2D cross-section offsets once and extruding them using `list.extend` significantly outperforms per-point checks (measured 40% speedup for filled, 7x for hollow).
**Action:** When generating 3D shapes with constant cross-sections, pre-calculate the 2D footprint and simply offset it for each layer to minimize arithmetic operations.
