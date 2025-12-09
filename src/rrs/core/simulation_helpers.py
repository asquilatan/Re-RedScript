"""Simulation helper functions for RRS DSL integration."""

from typing import Any
from rrs.core.simulation import SimulationEngine, SimulatedBlock
from rrs.core.module import Module


# Global simulation engine reference for helper functions
_current_simulation: SimulationEngine | None = None


def set_current_simulation(engine: SimulationEngine | None):
    """Set the global simulation engine reference."""
    global _current_simulation
    _current_simulation = engine


def ChangeState(block: SimulatedBlock | Module, property_name: str, value: Any) -> None:
    """Change a block's state property during simulation.
    
    Args:
        block: The block or module to modify
        property_name: Property to change (e.g., "powered", "extended")
        value: New value for the property
    
    Example:
        ChangeState(m.lever, "powered", True)
        ChangeState(piston, "extended", "true")
    """
    if _current_simulation is None:
        raise RuntimeError("ChangeState can only be called during simulation")
    
    # If it's a Module, try to find it in the simulation
    if isinstance(block, Module):
        simulated_block = _current_simulation.get_block(block.pos)
        if simulated_block is None:
            raise ValueError(f"Block not found in simulation at position {block.pos}")
        _current_simulation.change_state(simulated_block, property_name, value)
    elif isinstance(block, SimulatedBlock):
        _current_simulation.change_state(block, property_name, value)
    else:
        raise TypeError(f"ChangeState requires a Block or Module, got {type(block).__name__}")


def Trigger(module: Module) -> None:
    """Trigger a module's registered trigger block.
    
    Args:
        module: The module to trigger
        
    Example:
        Trigger(m)  # Invokes m's trigger block if defined
    """
    if _current_simulation is None:
        raise RuntimeError("Trigger can only be called during simulation")
    
    if not hasattr(module, 'trigger') or module.trigger is None:
        raise ValueError(f"Module '{module.id}' has no trigger defined")
    
    # The trigger is a callable that was set during module execution
    module.trigger()
