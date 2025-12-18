# Bolt's Journal

## 2024-05-22 - Deepcopy Bottleneck in Simulation
**Learning:** `copy.deepcopy` is extremely expensive for objects that contain mostly immutable primitives (like block properties in a Minecraft simulation).
**Action:** Always check if a shallow copy (`.copy()`) is sufficient before using `deepcopy`. In `SimulationEngine`, switching to shallow copy improved initialization time by ~40%.
