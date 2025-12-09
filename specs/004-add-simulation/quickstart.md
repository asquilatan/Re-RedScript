# Quickstart: Simulation

This guide explains how to use the new simulation features in RRS.

## Basic Simulation

To verify your Redstone logic, you can wrap your checks in a `Simulate` block.

```rrs
# Define your module
m = MyPistonDoor()

# Create a "Correct" module to compare against (state after simulation)
expected = MyPistonDoor()
# Manually set the expected state (e.g., piston extended)
expected.piston.extended = True
# Or use a helper if you have one

# Run Simulation for 20 ticks
Simulate((m, 20) => {
    # Trigger the input (e.g., a lever or observer)
    Trigger(m)
    
    # Or manually change state
    # ChangeState(m.input_lever, "powered", True)
    
    # Assertions
    # This checks if 'm' matches 'expected' at the end of 20 ticks
    assert(m, expected, "pos")
})
```

## Return Values

You can also use `Simulate` to get the result state or a success boolean.

```rrs
# Returns True if assertions pass, False otherwise
success = Simulate((m, 50) => {
    Trigger(m)
    assert(m, expected, "pos")
})

# Returns the modified module state (if no assertions block or explicit return)
# Note: Currently Simulate modifies 'm' in place in the scope, but future versions might return a copy.
```

## Debugging

If your simulation runs forever, ensure you provided a tick limit or your circuit stabilizes!
```rrs
# Infinite loop (careful!)
# Simulate(m) 
```
