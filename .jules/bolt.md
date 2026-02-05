## 2024-05-23 - Block.flatten Optimization
**Learning:** `copy.copy` overhead on simple objects like `Block` is significant (~600ms vs ~140ms for 100k calls). Manually cloning via `__new__` and `__dict__.copy()` yields a ~76% speedup, far exceeding the expected 35%. This suggests that for high-frequency object duplication in this codebase (like during flattening), avoiding standard copy mechanisms is critical.
**Action:** When cloning simple state-container objects in hot paths, prefer `__new__` + `__dict__` copy over `copy.copy`, provided `__slots__` are not used.

## 2026-01-07 - ConvertPicture Optimization
**Learning:** In nearest-neighbor search using Euclidean distance ($||p - q||^2 = ||p||^2 + ||q||^2 - 2 p \cdot q$), the term $||p||^2$ (query pixel energy) is constant for all candidates $. It can be omitted when only the index of the minimum distance () is required. This avoids one large broadcasting addition and the calculation of pixel sums, yielding a ~20% speedup for image conversion.
**Action:** When implementing nearest-neighbor searches where only the ranking matters, strip out constant terms from the distance metric to reduce operations.

## 2026-01-07 - ConvertPicture Optimization
**Learning:** In nearest-neighbor search using Euclidean distance ($||p - q||^2 = ||p||^2 + ||q||^2 - 2 p \cdot q$), the term $||p||^2$ (query pixel energy) is constant for all candidates $. It can be omitted when only the index of the minimum distance (argmin) is required. This avoids one large broadcasting addition and the calculation of pixel sums, yielding a ~20% speedup for image conversion.
**Action:** When implementing nearest-neighbor searches where only the ranking matters, strip out constant terms from the distance metric to reduce operations.

## 2026-02-04 - Hollow Cuboid Iteration
**Learning:** Python loop overhead is approximately 60ns per iteration. For O(N^3) algorithms like hollow cuboid generation, iterating the full volume just to check boundaries is wasteful. Reducing iteration to O(N^2) faces saved ~25% runtime purely by eliminating loop control overhead.
**Action:** For hollow shapes or shells, strictly iterate the surface coordinates using disjoint ranges rather than filtering a full volume scan.

## 2026-02-12 - Cylinder Rasterization Optimization
**Learning:** For extruded shapes like cylinders, pre-calculating the 2D cross-section offsets ($O(R^2)$) and extruding them via list addition is drastically faster than $O(H \times R^2)$ bounding box iteration with per-point distance checks (19x speedup observed). Additionally, accumulating points in a `list` instead of a `set` avoids hashing overhead when uniqueness is algorithmically guaranteed.
**Action:** Always prefer 2D pre-calculation + extrusion for translationally symmetric 3D shapes.
