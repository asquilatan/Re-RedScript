## 2024-05-23 - Block.flatten Optimization
**Learning:** `copy.copy` overhead on simple objects like `Block` is significant (~600ms vs ~140ms for 100k calls). Manually cloning via `__new__` and `__dict__.copy()` yields a ~76% speedup, far exceeding the expected 35%. This suggests that for high-frequency object duplication in this codebase (like during flattening), avoiding standard copy mechanisms is critical.
**Action:** When cloning simple state-container objects in hot paths, prefer `__new__` + `__dict__` copy over `copy.copy`, provided `__slots__` are not used.

## 2026-01-07 - ConvertPicture Optimization
**Learning:** In nearest-neighbor search using Euclidean distance ($||p - q||^2 = ||p||^2 + ||q||^2 - 2 p \cdot q$), the term $||p||^2$ (query pixel energy) is constant for all candidates $. It can be omitted when only the index of the minimum distance (argmin) is required. This avoids one large broadcasting addition and the calculation of pixel sums, yielding a ~20% speedup for image conversion.
**Action:** When implementing nearest-neighbor searches where only the ranking matters, strip out constant terms from the distance metric to reduce operations.

## 2026-01-22 - Cuboid Surface Iteration
**Learning:** Iterating the full volume ($O(N^3)$) to identify surface blocks for hollow shapes is a major bottleneck compared to direct surface iteration ($O(N^2)$), yielding ~7.8x speedup (1.12s -> 0.14s) for a 200^3 cube. However, direct surface iteration requires careful handling of face overlaps (corners/edges) to avoid duplicate block placements, as the underlying `Module` structure does not deduplicate entries.
**Action:** When generating hollow geometric shapes, iterate strictly over non-overlapping face coordinate sets instead of filtering a full volume scan.
