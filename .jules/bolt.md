## 2024-02-14 - Block Properties Copy
**Learning:** `copy.deepcopy` is excessively slow for flat dictionaries of primitives, which is the standard structure for block properties in this engine.
**Action:** Use `dict.copy()` (shallow copy) for block properties unless deep nesting is explicitly required by new features.
