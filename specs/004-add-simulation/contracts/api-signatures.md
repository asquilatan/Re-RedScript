# API Signatures: Add simulation functionalities

## Python API

### `src/rrs/core/simulation.py`

```python
class SimulationEngine:
    def __init__(self, module: Module, ticks: Optional[int] = None):
        """Initializes the simulation with a module."""
        pass

    def run(self) -> None:
        """Runs the simulation loop until max_ticks or empty queue."""
        pass

    def schedule(self, delay: int, priority: int, callback: Callable, *args):
        """Schedules an event."""
        pass

    def get_block(self, pos: Tuple[int, int, int]) -> Optional['SimulatedBlock']:
        """Returns the block at position."""
        pass

    def set_block(self, pos: Tuple[int, int, int], block: 'SimulatedBlock'):
        """Sets/Places a block."""
        pass
        
    def trigger_update(self, pos: Tuple[int, int, int]):
        """Notifies neighbors of an update."""
        pass
```

### `src/rrs/core/behaviors.py`

```python
class BlockBehavior:
    def on_tick(self, sim: SimulationEngine, pos: Tuple[int, int, int], block_state: Dict):
        pass

    def on_neighbor_update(self, sim: SimulationEngine, pos: Tuple[int, int, int], source_pos: Tuple[int, int, int]):
        pass

class ObserverBehavior(BlockBehavior):
    pass

class PistonBehavior(BlockBehavior):
    pass
# ... and so on
```

### `src/rrs/dsl/interpreter.py`

```python
class Interpreter:
    # Existing methods...

    def func_Simulate(self, module, ticks=None, assertion_block=None):
        """
        Built-in function: Simulate(module, ticks) => { ... }
        """
        pass

    def func_Trigger(self, module):
        """
        Built-in function: Trigger(module)
        """
        pass
        
    def func_ChangeState(self, block, property, value):
        """
        Built-in function: ChangeState(block, prop, val)
        """
        pass
```
