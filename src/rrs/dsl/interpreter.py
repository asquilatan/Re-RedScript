import os
import rrs
from rrs.core.module import Module
from rrs.core.block import Block
from rrs.dsl.ast import (
    Program, ModuleDef, FunctionCall, Literal, Variable, BinaryOp, TupleExpr,
    Assignment, AugAssignment, ListExpr, ForLoop, FuncDef, ReturnStmt, ImportStmt, FromImportStmt,
    MethodCall, GetAttr, ExprStmt, Arg, Kwarg
)
from typing import Dict, Any, List, Optional

class ModuleNamespace:
    """Simple wrapper exposing interpreter globals as module-like attributes."""

    def __init__(self, symbols):
        self.__dict__.update(symbols)


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

    def __init__(self, import_cache=None, import_stack=None):
        self.globals = SymbolTable()
        self.register_builtins()
        self.current_module: Optional[Module] = None 
        self.modules_registry = {} 
        self.current_scope = self.globals
        self.import_cache = import_cache if import_cache is not None else {}
        self.import_stack = import_stack if import_stack is not None else []
        self._module_counter = 0

    def register_builtins(self):
        """Populate the global scope with built-in block factories and helpers."""
        import math
        import random
        
        # Basic Blocks
        self.globals.set("Piston", rrs.Piston)
        self.globals.set("Repeater", rrs.Repeater)
        self.globals.set("Stone", rrs.Stone)
        self.globals.set("Block", Block)
        self.globals.set("Observer", rrs.Observer)
        
        # Decorative Blocks
        self.globals.set("GoldBlock", rrs.GoldBlock)
        self.globals.set("DiamondBlock", rrs.DiamondBlock)
        self.globals.set("EmeraldBlock", rrs.EmeraldBlock)
        self.globals.set("Glowstone", rrs.Glowstone)
        self.globals.set("SeaLantern", rrs.SeaLantern)
        self.globals.set("RedstoneBlock", rrs.RedstoneBlock)
        self.globals.set("LapisBlock", rrs.LapisBlock)
        self.globals.set("IronBlock", rrs.IronBlock)
        
        # Functions
        self.globals.set("range", range)
        self.globals.set("print", print)  # For debugging
        self.globals.set("Module", self._create_module)
        
        # Math functions
        self.globals.set("sin", math.sin)
        self.globals.set("cos", math.cos)
        self.globals.set("floor", lambda x: int(math.floor(x)))
        self.globals.set("abs", abs)
        self.globals.set("PI", math.pi)
        
        # Random functions
        self.globals.set("random", random.random)
        self.globals.set("randint", random.randint)

    def _next_module_id(self):
        self._module_counter += 1
        return f"anon_module_{self._module_counter}"

    def _create_module(self, id=None, pos=(0,0,0), size=(1,1,1), **kwargs):
        """Factory exposed to scripts for manual Module instantiation."""
        if id is None:
            id = self._next_module_id()
        return Module(id, pos=pos, size=size, **kwargs)

    def run(self, program: Program) -> List[Module]:
        # Register ModuleDefs first
        for stmt in program.statements:
            if isinstance(stmt, ModuleDef):
                self.visit_ModuleDef(stmt)
        
        results = []
        for stmt in program.statements:
            if not isinstance(stmt, ModuleDef):
                res = self.visit(stmt)
                if isinstance(res, Module):
                    results.append(res)
        return results

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{node.__class__.__name__} method")

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

    def visit_ExprStmt(self, node: ExprStmt):
        return self.visit(node.expr)

    def visit_Assignment(self, node: Assignment):
        val = self.evaluate(node.value)
        self.current_scope.set(node.target, val)

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

    def visit_FuncDef(self, node: FuncDef):
        self.current_scope.set(node.name, UserFunction(node, self.current_scope))

    def visit_ReturnStmt(self, node: ReturnStmt):
        value = None
        if node.value:
            value = self.evaluate(node.value)
        raise ReturnException(value)

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
            if hasattr(module_exports, name):
                val = getattr(module_exports, name)
                self.current_scope.set(name, val)
            else:
                raise ImportError(f"cannot import name '{name}' from '{module_name}'")

    def load_module(self, module_name):
        # Lazy import to avoid circular dependency
        from rrs.dsl.parser import RRSParser
        
        filename = f"{module_name}.rrs"
        if module_name in self.import_stack:
            chain = " -> ".join(self.import_stack + [module_name])
            raise ImportError(f"Circular import detected: {chain}")
        if not os.path.exists(filename):
             raise ImportError(f"Module {module_name} not found at {os.path.abspath(filename)}")
             
        parser = RRSParser()
        self.import_stack.append(module_name)
        try:
            program = parser.parse_file(filename)
            nested = Interpreter(import_cache=self.import_cache, import_stack=self.import_stack)
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
            # Imported DSL module - call it and add result to current module
            result = obj(*eval_args, **eval_kwargs)
            if isinstance(result, Module) and self.current_module:
                self.current_module.add(result)
            return result
        elif obj:
            # Builtin Block class or function
            # If it's a Block class (like Piston), instantiating it returns a Block instance.
            # If we are inside a module, we should add it to the module.
            result = obj(*eval_args, **eval_kwargs)
            
            if isinstance(result, rrs.core.block.Block) and self.current_module:
                self.current_module.add(result)
            
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
        
        if len(args) != len(def_node.params):
             raise ValueError(f"Module {name} expects {len(def_node.params)} args, got {len(args)}")
             
        # Create new scope for module execution
        prev_scope = self.current_scope
        self.current_scope = SymbolTable(parent=self.globals) # Module scope usually isolated from caller, but has access to globals
        
        for param, val in zip(def_node.params, args):
            self.current_scope.set(param, val)
            
        pos = kwargs.get('pos', (0,0,0))
        module_instance = Module(name, pos=pos)
        
        prev_module = self.current_module
        self.current_module = module_instance
        
        returned = None
        try:
            for stmt in def_node.body:
                self.visit(stmt)
        except ReturnException as ret:
            returned = ret.value
        finally:
            self.current_module = prev_module
            self.current_scope = prev_scope
            
        module_result = self._resolve_module_return(module_instance, returned)
        
        # If called from another module, add it
        if self.current_module:
            self.current_module.add(module_result)
            
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
