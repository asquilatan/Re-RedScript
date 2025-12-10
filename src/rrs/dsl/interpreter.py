import os
import rrs
from rrs.core.module import Module
from rrs.core.block import Block
from rrs.dsl.ast import (
    Program, ModuleDef, FunctionCall, Literal, Variable, BinaryOp, TupleExpr,
    Assignment, AugAssignment, ListExpr, ForLoop, FuncDef, ReturnStmt, ImportStmt, FromImportStmt,
    MethodCall, GetAttr, ExprStmt, Arg, Kwarg, AssertStmt, SimulateStmt, TriggerBlock,
    IfStmt, WhileLoop, IndexExpr, IndexAssignment, UnaryOp, DictExpr
)
from typing import Dict, Any, List, Optional
import sys

class ModuleNamespace:
    """Simple wrapper exposing interpreter globals as module-like attributes.
       Also used for wrapping internal Python objects (like StdLib) to look like modules.
    """
    def __init__(self, globals_dict):
        self._globals = globals_dict

    def __getattr__(self, name):
        # Support dict access or attribute access
        if isinstance(self._globals, dict):
            if name in self._globals:
                return self._globals[name]
        elif hasattr(self._globals, name):
             return getattr(self._globals, name)
             
        raise AttributeError(f"Module has no attribute '{name}'")


class UserFunction:
    """Captures a DSL function definition along with its lexical scope."""

    def __init__(self, node: FuncDef, closure: 'SymbolTable'):
        self.node = node
        self.closure = closure


class ModuleFactory:
    """Wraps a DSL module definition for export, making it callable."""

    def __init__(self, node: ModuleDef, interpreter: 'Interpreter'):
        self.node = node
        self.interpreter = interpreter

    def __call__(self, *args, **kwargs):
        return self.interpreter.execute_module(self.node.name, list(args), kwargs)


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class SymbolTable:
    """Nested dictionary structure used to model lexical scopes."""
    def __init__(self, parent=None):
        self.symbols: Dict[str, Any] = {}
        self.parent = parent

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.get(name)
        return None

    def set(self, name, value):
        self.symbols[name] = value

class Interpreter:
    """Executes RRS AST nodes by walking them with a visitor."""

    def __init__(self, import_cache=None, import_stack=None, base_dir=None):
        self.globals = SymbolTable()
        self.current_module: Optional[Module] = None 
        self.modules_registry = {} 
        self.current_scope = self.globals
        self.import_cache = import_cache if import_cache is not None else {}
        self.import_stack = import_stack if import_stack is not None else []
        self.base_dir = base_dir if base_dir is not None else os.getcwd() # Default to CWD if not specified
        self._module_counter = 0
        self.exports: List[Module] = []  # Modules marked for export
        self._auto_add = True  # Whether to auto-add blocks to current module
        # Active SimulationEngine when executing within a Simulate() block
        self._current_simulation = None
        self.register_builtins()

    def register_builtins(self):
        import math
        import random
        
        # Functions
        self.globals.set("range", range)
        self.globals.set("print", print)
        self.globals.set("Module", self._create_module)
        
        # Boolean/None literals
        self.globals.set("True", True)
        self.globals.set("False", False)
        self.globals.set("None", None)
        
        # Math functions
        self.globals.set("sin", math.sin)
        self.globals.set("cos", math.cos)
        self.globals.set("tan", math.tan)
        self.globals.set("asin", math.asin)
        self.globals.set("acos", math.acos)
        self.globals.set("atan", math.atan)
        self.globals.set("atan2", math.atan2)
        self.globals.set("sqrt", math.sqrt)
        self.globals.set("pow", math.pow)
        self.globals.set("exp", math.exp)
        self.globals.set("log", math.log)
        self.globals.set("log10", math.log10)
        self.globals.set("floor", lambda x: int(math.floor(x)))
        self.globals.set("ceil", lambda x: int(math.ceil(x)))
        self.globals.set("round", round)
        self.globals.set("abs", abs)
        self.globals.set("min", min)
        self.globals.set("max", max)
        self.globals.set("PI", math.pi)
        self.globals.set("E", math.e)
        
        # List functions
        self.globals.set("len", len)
        self.globals.set("list", list)
        self.globals.set("append", lambda lst, item: lst.append(item) or lst)
        self.globals.set("pop", lambda lst: lst.pop())
        self.globals.set("insert", lambda lst, i, item: lst.insert(i, item) or lst)
        
        # Type conversion
        self.globals.set("str", str)
        self.globals.set("int", int)
        self.globals.set("float", float)
        self.globals.set("bool", bool)
        
        # Random functions
        self.globals.set("random", random.random)
        self.globals.set("randint", random.randint)
        
        # Assertion
        from rrs.core.assertion import rrs_assert
        self.globals.set("assert", rrs_assert)
        
        # Export function
        self.globals.set("export", self._export_module)
        
        # Add function - explicitly add block/module to current module
        self.globals.set("add", self._add_to_current_module)

        # Simulation helpers
        self.globals.set("Simulate", self.func_Simulate)
        self.globals.set("ChangeState", self.func_ChangeState)

        # Standard Library Injection
        # We assume 'std' module is available. We inject it into the import cache directly.
        from rrs.stdlib import StdLib
        stdlib = StdLib(self)
        
        # Inject 'std' into cached modules so 'import std' finds it
        # We wrap it in a ModuleNamespace-like object or just use the object if getattr works
        # Current ModuleNamespace expects a dict, let's update it or wrap stdlib.
        # Check if ModuleNamespace supports objects? No, it expects dict.
        # I updated ModuleNamespace above to support objects.
        self.import_cache['std'] = ModuleNamespace(stdlib)

        # Inject new modules: std.line, std.figure, std.img
        import rrs.stdlib.line as std_line
        import rrs.stdlib.figure as std_figure
        import rrs.stdlib.img as std_img

        self.import_cache['std.line'] = ModuleNamespace(std_line)
        self.import_cache['std.figure'] = ModuleNamespace(std_figure)
        self.import_cache['std.img'] = ModuleNamespace(std_img)

        # Auto-generated registrations
        self.globals.set("Block", Block)
        
        # Load Standard Blocks dynamically
        from rrs.stdlib.stdblocks import get_standard_blocks
        std_blocks = get_standard_blocks()
        for name, cls in std_blocks.items():
            self.globals.set(name, cls)

        # Load User Blocks if blocks.json exists in base_dir
        from rrs.core.block import load_blocks_from_json
        if self.base_dir:
            user_blocks_path = os.path.join(self.base_dir, "blocks.json")
            if os.path.exists(user_blocks_path):
                 user_blocks = load_blocks_from_json(user_blocks_path)
                 for name, cls in user_blocks.items():
                     self.globals.set(name, cls)
    def _next_module_id(self):
        self._module_counter += 1
        return f"anon_module_{self._module_counter}"

    def _create_module(self, id=None, pos=(0,0,0), size=(1,1,1), **kwargs):
        """Factory exposed to scripts for manual Module instantiation."""
        if id is None:
            id = self._next_module_id()
        return Module(id, pos=pos, size=size, **kwargs)

    def _export_module(self, module: Module):
        """Mark a module for export. Called via export(m) in RRS scripts."""
        if not isinstance(module, Module):
            raise TypeError(f"export() requires a Module, got {type(module).__name__}")
        self.exports.append(module)
        return module

    def _add_to_current_module(self, item):
        """Add a block or module to the current module. Called via add(item) in RRS scripts."""
        if self.current_module is None:
            raise RuntimeError("add() can only be called inside a module definition")
        
        if isinstance(item, (Block, Module)):
            self.current_module.add(item)
            return item
        else:
            raise TypeError(f"add() requires a Block or Module, got {type(item).__name__}")

    # ------------------------------------------------------------------
    # Simulation builtins
    # ------------------------------------------------------------------

    def func_Simulate(self, module: Module, ticks: Optional[int] = None, assertion_block=None):
        """Built-in function: Simulate(module, ticks=None, assertion_block=None).

        This is a thin wrapper around :class:`SimulationEngine`.  When an
        ``assertion_block`` callable is provided it is executed after the
        simulation; the return value is ``True`` if all assertions pass
        and ``False`` if an :class:`AssertionError` is raised.
        """
        from rrs.core.simulation import SimulationEngine

        if not isinstance(module, Module):
            raise TypeError(f"Simulate() expects a Module, got {type(module).__name__}")

        engine = SimulationEngine(module, ticks=ticks)
        prev_engine = self._current_simulation
        self._current_simulation = engine
        try:
            engine.run()

            if assertion_block is None:
                # No special assertion handling requested; return the
                # (potentially modified) module like a normal function.
                return module

            # Python-side assertions block: expected to raise
            # AssertionError on failure.
            try:
                if callable(assertion_block):
                    assertion_block(engine)
                return True
            except AssertionError:
                return False
        finally:
            self._current_simulation = prev_engine

    def func_Trigger(self, module: Module):
        """Built-in function: Trigger(module).

        If called inside a Simulate() context it uses the active
        SimulationEngine; otherwise a temporary engine is created.
        """
        from rrs.core.simulation import SimulationEngine

        if not isinstance(module, Module):
            raise TypeError(f"Trigger() expects a Module, got {type(module).__name__}")

        engine = self._current_simulation or SimulationEngine(module, ticks=None)

        # Naive implementation: notify all blocks in the module.  More
        # sophisticated scenarios can pass smaller modules.
        for blk in module.flatten():
            if isinstance(blk, Block):
                engine.trigger_update(blk.pos)

        engine.run()

        # Outside of a simulation context we simply return the module so
        # that scripts can chain calls if they wish.
        return module

    def func_ChangeState(self, block: Block, property: str, value):
        """Built-in function: ChangeState(block, prop, val).

        During a Simulate() call this mutates the corresponding
        SimulatedBlock's properties in the active SimulationEngine.
        """
        if not isinstance(block, Block):
            raise TypeError(f"ChangeState() expects a Block, got {type(block).__name__}")

        engine = self._current_simulation
        if engine is None:
            raise RuntimeError("ChangeState() can only be used inside Simulate()")

        sim_block = engine.get_block(block.pos)
        if sim_block is None:
            raise ValueError(f"No simulated block found at position {block.pos}")

        sim_block.properties[property] = value
        return block

    def run(self, program: Program) -> List[Module]:
        # Register ModuleDefs first
        for stmt in program.statements:
            if isinstance(stmt, ModuleDef):
                self.visit_ModuleDef(stmt)

        for stmt in program.statements:
            if not isinstance(stmt, ModuleDef):
                self.visit(stmt)
        
        # Return explicitly exported modules
        return self.exports

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{node.__class__.__name__} method")

    def visit_SimulateStmt(self, node: SimulateStmt):
        """Handle Simulate((module, ticks) => { ... }) syntax.
        
        Executes body statements within a simulation context.
        If an AssertionError occurs and result is not assigned,
        prints error and exits with code 1.
        """
        from rrs.core.simulation import SimulationEngine
        
        # Get the module variable
        module = self.current_scope.get(node.module_var)
        if not isinstance(module, Module):
            raise TypeError(f"Simulate() expects a Module, got {type(module).__name__}")
        
        # Get tick count
        ticks = None
        if node.ticks is not None:
            ticks = self.evaluate(node.ticks)
        
        # Create simulation engine
        engine = SimulationEngine(module, ticks=ticks)
        prev_engine = self._current_simulation
        self._current_simulation = engine
        
        has_assert = False
        assertion_failed = False
        
        try:
            engine.run()
            
            # Execute body statements
            for stmt in node.body:
                if isinstance(stmt, AssertStmt):
                    has_assert = True
                self.visit(stmt)
        except AssertionError as e:
            assertion_failed = True
            # Print error and exit with code 1
            print(f"Simulation assertion failed: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            self._current_simulation = prev_engine
        
        # Return based on assert behavior
        if has_assert:
            return not assertion_failed
        return module

    def visit_Program(self, node: Program):
        # Register ModuleDefs first
        for stmt in node.statements:
            if isinstance(stmt, ModuleDef):
                self.visit_ModuleDef(stmt)

        # Execute other statements
        last_result = None
        for stmt in node.statements:
            if not isinstance(stmt, ModuleDef):
                last_result = self.visit(stmt)

        return last_result

    def visit_ModuleDef(self, node: ModuleDef):
        self.modules_registry[node.name] = node
        # Register in current scope as a callable factory
        factory = ModuleFactory(node, self)
        self.current_scope.set(node.name, factory)

    def visit_ExprStmt(self, node: ExprStmt):
        # Expression statements auto-add blocks/modules
        prev_auto_add = self._auto_add
        self._auto_add = True
        result = self.evaluate(node.expr)
        self._auto_add = prev_auto_add
        
        # If result is a Block or Module and we're in a module, add it
        if self.current_module and isinstance(result, (Block, Module)):
            # Check if it was already added (e.g. by add() function called in expr)
            # We assume if it's the last child, it was just added.
            if not self.current_module.children or self.current_module.children[-1] is not result:
                self.current_module.add(result)
        return result

    def visit_Assignment(self, node: Assignment):
        # Assignments do NOT auto-add
        prev_auto_add = self._auto_add
        self._auto_add = False
        val = self.evaluate(node.value)
        self._auto_add = prev_auto_add
        self.current_scope.set(node.target, val)
        
        # Register blocks in module's block registry for name-based access
        if self.current_module and isinstance(val, (Block, Module)):
            self.current_module.register_block(node.target, val)
            # Do NOT auto-add to module children on assignment. 
            # User must use add() or standalone expression if they want it in the layout.
            # self.current_module.add(val)

    def visit_AugAssignment(self, node: AugAssignment):
        current = self.current_scope.get(node.target)
        if current is None:
            raise NameError(f"Undefined variable: {node.target}")
        delta = self.evaluate(node.value)
        if node.op == '+=':
            updated = self._apply_plus_equal(current, delta)
        else:
            raise NotImplementedError(f"Unsupported augmented assignment operator {node.op}")
        self.current_scope.set(node.target, updated)

    def visit_ForLoop(self, node: ForLoop):
        iterable = self.evaluate(node.iterable)
        # iterable should be iterable

        for item in iterable:
            self.current_scope.set(node.target, item)
            for stmt in node.body:
                self.visit(stmt)

    def visit_WhileLoop(self, node: WhileLoop):
        while self.evaluate(node.condition):
            for stmt in node.body:
                self.visit(stmt)

    def visit_IfStmt(self, node: IfStmt):
        if self.evaluate(node.condition):
            for stmt in node.body:
                self.visit(stmt)
            return
        
        # Check elif clauses
        for elif_cond, elif_body in node.elif_clauses:
            if self.evaluate(elif_cond):
                for stmt in elif_body:
                    self.visit(stmt)
                return
        
        # Else clause
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)

    def visit_IndexAssignment(self, node: IndexAssignment):
        obj = self.evaluate(node.obj)
        index = self.evaluate(node.index)
        value = self.evaluate(node.value)
        obj[index] = value

    def visit_FuncDef(self, node: FuncDef):
        self.current_scope.set(node.name, UserFunction(node, self.current_scope))

    def visit_ReturnStmt(self, node: ReturnStmt):
        value = None
        if node.value:
            value = self.evaluate(node.value)
        raise ReturnException(value)

    def visit_AssertStmt(self, node: AssertStmt):
        test_val = self.evaluate(node.test)
        if not test_val:
            msg = "Assertion failed"
            if node.msg:
                msg = str(self.evaluate(node.msg))
            raise AssertionError(msg)

    def visit_ImportStmt(self, node: ImportStmt):
        module_name = node.module_name
        alias = node.alias or module_name

        if module_name in self.import_cache:
            module_exports = self.import_cache[module_name]
        else:
            module_exports = self.load_module(module_name)
            self.import_cache[module_name] = module_exports

        self.current_scope.set(alias, module_exports)

    def visit_FromImportStmt(self, node: FromImportStmt):
        module_name = node.module_name

        if module_name in self.import_cache:
            module_exports = self.import_cache[module_name]
        else:
            module_exports = self.load_module(module_name)
            self.import_cache[module_name] = module_exports

        for name in node.names:
            if name == '*':
                # Import all public names
                if hasattr(module_exports, '_globals'): # ModuleNamespace
                    # For ModuleNamespace/virtual modules
                     source = module_exports._globals
                     if isinstance(source, dict):
                         iterator = source.keys()
                     else:
                         iterator = dir(source)
                     
                     for key in iterator:
                         if not key.startswith('_'):
                             val = getattr(module_exports, key)
                             self.current_scope.set(key, val)
                else:
                    # For compiled RRS modules (Module object or dict?)
                    # If it's a Module/ModuleNamespace
                    # We might need to handle different types.
                    # Assuming it behaves like an object or dict context.
                     iterator = dir(module_exports)
                     for key in iterator:
                         if not key.startswith('_'):
                             val = getattr(module_exports, key)
                             self.current_scope.set(key, val)
            else:
                if hasattr(module_exports, name):
                    val = getattr(module_exports, name)
                    self.current_scope.set(name, val)
                else:
                    raise ImportError(f"Module '{module_name}' has no attribute '{name}'")

    def load_module(self, module_name):
        # Lazy import to avoid circular dependency
        from rrs.dsl.parser import RRSParser

        filename = os.path.join(self.base_dir, f"{module_name}.rrs")
        
        # Also check current working directory as fallback if relative lookup fails
        if not os.path.exists(filename):
             cwd_filename = f"{module_name}.rrs"
             if os.path.exists(cwd_filename):
                 filename = cwd_filename

        if module_name in self.import_stack:
            chain = " -> ".join(self.import_stack + [module_name])
            raise ImportError(f"Circular import detected: {chain}")
        if not os.path.exists(filename):
             raise ImportError(f"Module {module_name} not found at {os.path.abspath(filename)}")

        parser = RRSParser()
        self.import_stack.append(module_name)
        try:
            program = parser.parse_file(filename)
            # Create nested interpreter with updated base_dir (directory of the imported module)
            nested_base_dir = os.path.dirname(os.path.abspath(filename))
            nested = Interpreter(import_cache=self.import_cache, import_stack=self.import_stack, base_dir=nested_base_dir)
            nested.run(program)

            # Merge globals and user-defined modules into exports
            # User-defined modules need to be wrapped so they can be called
            all_exports = dict(nested.globals.symbols)
            for mod_name, mod_def in nested.modules_registry.items():
                # Create a callable factory for this module definition
                all_exports[mod_name] = ModuleFactory(mod_def, nested)

            exports = ModuleNamespace(all_exports)
        finally:
            self.import_stack.pop()

        return exports

    def visit_FunctionCall(self, node: FunctionCall):
        func_name = node.name
        obj = self.current_scope.get(func_name)

        eval_args = [self.evaluate(arg.value) for arg in node.args]
        eval_kwargs = {kw.name: self.evaluate(kw.value) for kw in node.kwargs}

        if isinstance(obj, UserFunction):
            return self.execute_function(obj, eval_args, eval_kwargs)
        elif isinstance(obj, ModuleFactory):
            # Imported DSL module
            result = obj(*eval_args, **eval_kwargs)
            return result
        elif obj:
            # Builtin Block class or function
            result = obj(*eval_args, **eval_kwargs)
            return result

        elif func_name in self.modules_registry:
            # User defined module
            return self.execute_module(func_name, eval_args, eval_kwargs)
        else:
            raise NameError(f"Unknown block or module: {func_name}")

    def execute_function(self, func_obj: UserFunction, args: List[Any], kwargs: Dict[str, Any]):
        func_def = func_obj.node
        if len(args) != len(func_def.params):
             raise ValueError(f"Function {func_def.name} expects {len(func_def.params)} args, got {len(args)}")

        prev_scope = self.current_scope
        self.current_scope = SymbolTable(parent=func_obj.closure)

        for param, val in zip(func_def.params, args):
            self.current_scope.set(param, val)

        try:
            for stmt in func_def.body:
                self.visit(stmt)
        except ReturnException as e:
            return e.value
        finally:
            self.current_scope = prev_scope

        return None

    def execute_module(self, name: str, args: List[Any], kwargs: Dict[str, Any]) -> Module:
        def_node = self.modules_registry[name]

        if len(args) > len(def_node.params):
             raise ValueError(f"Module {name} expects at most {len(def_node.params)} args, got {len(args)}")
        
        # Create new scope for module execution
        prev_scope = self.current_scope
        self.current_scope = SymbolTable(parent=self.globals)

        # Bind arguments
        bound_args = {}
        # 1. Bind positional args
        for i, val in enumerate(args):
            param = def_node.params[i]
            bound_args[param] = val
        
        # 2. Bind keyword args
        for param in def_node.params:
            if param in kwargs:
                if param in bound_args:
                     raise ValueError(f"Module {name} got multiple values for argument '{param}'")
                bound_args[param] = kwargs[param]
            elif param not in bound_args:
                 # Check if we can proceed (maybe optional?) RRS doesn't support defaults yet?
                 # Assuming all params required for now (unless 'pos' is special?)
                 # Actually 'pos' is usually implicit in Module constructor if NOT defined in params, 
                 # but here it IS defined.
                 raise ValueError(f"Module {name} missing required argument '{param}'")
                 
        for param, val in bound_args.items():
            self.current_scope.set(param, val)

        pos = kwargs.get('pos', (0,0,0))
        module_instance = Module(name, pos=pos)

        prev_module = self.current_module
        self.current_module = module_instance

        returned = None
        module_scope = None
        try:
            for stmt in def_node.body:
                self.visit(stmt)
            # Capture scope before exiting
            module_scope = self.current_scope
        except ReturnException as ret:
            returned = ret.value
            module_scope = self.current_scope
        finally:
            self.current_module = prev_module
            self.current_scope = prev_scope

        module_result = self._resolve_module_return(module_instance, returned)

        # Populate module exports from the executed scope
        if isinstance(module_result, Module) and module_scope:
            for name, val in module_scope.symbols.items():
                if not name.startswith('_'):
                    module_result.exports[name] = val

        # Auto-add is now handled by visit_ExprStmt, not here
        return module_result

    def visit_GetAttr(self, node: GetAttr):
        obj = self.evaluate(node.obj)
        if hasattr(obj, node.attr):
            return getattr(obj, node.attr)
        raise AttributeError(f"Object {obj} has no attribute {node.attr}")

    def visit_MethodCall(self, node: MethodCall):
        obj = self.evaluate(node.obj)
        method_name = node.method

        if hasattr(obj, method_name):
            method = getattr(obj, method_name)

            eval_args = [self.evaluate(arg.value) for arg in node.args]
            eval_kwargs = {kw.name: self.evaluate(kw.value) for kw in node.kwargs}

            if isinstance(method, UserFunction):
                return self.execute_function(method, eval_args, eval_kwargs)
            elif isinstance(method, ModuleFactory):
                # Imported DSL module accessed via namespace (e.g., library.ImportedModule)
                result = method(*eval_args, **eval_kwargs)
                if isinstance(result, Module) and self.current_module:
                    self.current_module.add(result)
                return result
            elif callable(method):
                result = method(*eval_args, **eval_kwargs)
                # Also add to current module if result is a Module
                if isinstance(result, Module) and self.current_module:
                    self.current_module.add(result)
                return result
            else:
                raise TypeError(f"Attribute {method_name} is not callable")
        else:
             raise AttributeError(f"Object {obj} has no attribute {method_name}")

    def evaluate(self, expr, scope=None):
        if scope is None: scope = self.current_scope

        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Variable):
            val = scope.get(expr.name)
            if val is None:
                  raise NameError(f"Undefined variable: {expr.name}")
            return val
        elif isinstance(expr, BinaryOp):
            l = self.evaluate(expr.left, scope)
            r = self.evaluate(expr.right, scope)
            if expr.op == '+': return l + r
            if expr.op == '-': return l - r
            if expr.op == '*': return l * r
            if expr.op == '/': return l / r
            if expr.op == '%': return l % r
            if expr.op == '==': return l == r
            if expr.op == '!=': return l != r
            if expr.op == '<': return l < r
            if expr.op == '>': return l > r
            if expr.op == '<=': return l <= r
            if expr.op == '<=': return l <= r
            if expr.op == '>=': return l >= r
            # Boolean operators
            if expr.op == 'and': return l and r
            if expr.op == 'or': return l or r
        elif isinstance(expr, TupleExpr):
            return tuple(self.evaluate(e, scope) for e in expr.elements)
        elif isinstance(expr, ListExpr):
            return [self.evaluate(e, scope) for e in expr.elements]
        elif isinstance(expr, FunctionCall):
            # Function call as expression (e.g. range(3))
            return self.visit_FunctionCall(expr)
        elif isinstance(expr, MethodCall):
            return self.visit_MethodCall(expr)
        elif isinstance(expr, GetAttr):
            return self.visit_GetAttr(expr)
        elif isinstance(expr, IndexExpr):
            obj = self.evaluate(expr.obj, scope)
            index = self.evaluate(expr.index, scope)
            return obj[index]
        elif isinstance(expr, UnaryOp):
            operand = self.evaluate(expr.operand, scope)
            if expr.op == '-':
                return -operand
            elif expr.op == '+':
                return +operand
            elif expr.op == 'not':
                return not operand
        elif isinstance(expr, DictExpr):
            d = {}
            for k_expr, v_expr in expr.pairs:
                k = self.evaluate(k_expr, scope)
                v = self.evaluate(v_expr, scope)
                d[k] = v
            return d

        return None

    def _apply_plus_equal(self, current, delta):
        """Best-effort implementation of "+=" used by the DSL's module syntax."""
        if hasattr(current, '__iadd__'):
            result = current.__iadd__(delta)
            if result is NotImplemented:
                raise TypeError("Unsupported '+=' operation for given operands")
            return result
        try:
            return current + delta
        except Exception as exc:
            raise TypeError("Unsupported '+=' operation for given operands") from exc

    def _resolve_module_return(self, default_module: Module, returned_value):
        """Determine which module should bubble up from a module block."""
        if returned_value is None:
            return default_module
        if isinstance(returned_value, Module):
            return returned_value
        raise TypeError("Module blocks must return a Module instance")
