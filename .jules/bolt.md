## 2024-03-24 - Efficient Object Copying for Dynamic Classes
**Learning:** `copy.copy` overhead is significant (35% slower) compared to manual copying for simple objects, but manual instantiation `Class(id, **props)` fails for dynamic subclasses with different `__init__` signatures.
**Action:** Use `cls.__new__(cls)` and update `__dict__` manually to bypass `__init__` when optimizing copy operations for class hierarchies with inconsistent constructors.
