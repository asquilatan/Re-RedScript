## 2024-05-23 - Block.flatten Optimization
**Learning:** `copy.copy` overhead on simple objects like `Block` is significant (~600ms vs ~140ms for 100k calls). Manually cloning via `__new__` and `__dict__.copy()` yields a ~76% speedup, far exceeding the expected 35%. This suggests that for high-frequency object duplication in this codebase (like during flattening), avoiding standard copy mechanisms is critical.
**Action:** When cloning simple state-container objects in hot paths, prefer `__new__` + `__dict__` copy over `copy.copy`, provided `__slots__` are not used.

## 2024-05-23 - Recursive List Flattening Optimization
**Learning:** Recursive list construction using `list.extend(recursive_call())` incurs significant overhead due to intermediate list creation and allocation. Replacing this with an accumulator pattern (passing a single list reference down via `_flatten_into`) avoids these intermediate allocations.
**Impact:** ~25% speedup in `Module.flatten()` for deep/wide hierarchies.
**Action:** For recursive aggregation methods (flattening, collecting nodes), prefer passing a mutable accumulator (list, set) rather than returning and concatenating new collections at each level.
