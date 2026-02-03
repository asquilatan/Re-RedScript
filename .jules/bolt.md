## 2024-05-23 - Block.flatten Optimization
**Learning:** `copy.copy` overhead on simple objects like `Block` is significant (~600ms vs ~140ms for 100k calls). Manually cloning via `__new__` and `__dict__.copy()` yields a ~76% speedup, far exceeding the expected 35%. This suggests that for high-frequency object duplication in this codebase (like during flattening), avoiding standard copy mechanisms is critical.
**Action:** When cloning simple state-container objects in hot paths, prefer `__new__` + `__dict__` copy over `copy.copy`, provided `__slots__` are not used.

## 2026-01-07 - ConvertPicture Optimization
**Learning:** In nearest-neighbor search using Euclidean distance ($||p - q||^2 = ||p||^2 + ||q||^2 - 2 p \cdot q$), the term $||p||^2$ (query pixel energy) is constant for all candidates $. It can be omitted when only the index of the minimum distance (argmin) is required. This avoids one large broadcasting addition and the calculation of pixel sums, yielding a ~20% speedup for image conversion.
**Action:** When implementing nearest-neighbor searches where only the ranking matters, strip out constant terms from the distance metric to reduce operations.

## 2026-02-03 - ConvertPicture Optimization II
**Learning:** `place_in_module` is a convenience wrapper that introduces significant overhead (function call + `isinstance` checks) inside tight loops (like pixel iteration). Bypassing it and directly instantiating `Block` yielded a ~4x speedup (from ~1.8s to ~0.45s for 256x256 images).
**Action:** In performance-critical loops, avoid generic helper functions that perform type checking. Use direct instantiation or specialized functions.
