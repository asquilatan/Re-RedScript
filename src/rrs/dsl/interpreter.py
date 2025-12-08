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
        self.globals.set("StickyPiston", rrs.StickyPiston)
        self.globals.set("RedstoneTorch", rrs.RedstoneTorch)
        self.globals.set("RedstoneLamp", rrs.RedstoneLamp)
        self.globals.set("NoteBlock", rrs.NoteBlock)
        self.globals.set("Dispenser", rrs.Dispenser)
        self.globals.set("Dropper", rrs.Dropper)
        self.globals.set("Hopper", rrs.Hopper)
        self.globals.set("Comparator", rrs.Comparator)
        self.globals.set("Target", rrs.Target)
        self.globals.set("Lever", rrs.Lever)
        self.globals.set("LightningRod", rrs.LightningRod)
        self.globals.set("DaylightDetector", rrs.DaylightDetector)
        self.globals.set("SculkSensor", rrs.SculkSensor)
        self.globals.set("TripwireHook", rrs.TripwireHook)
        self.globals.set("TrappedChest", rrs.TrappedChest)
        self.globals.set("TNT", rrs.TNT)
        self.globals.set("RedstoneWire", rrs.RedstoneWire)
        self.globals.set("OakButton", rrs.OakButton)
        self.globals.set("StoneButton", rrs.StoneButton)
        self.globals.set("OakPressurePlate", rrs.OakPressurePlate)
        self.globals.set("StonePressurePlate", rrs.StonePressurePlate)
        self.globals.set("LightWeightedPressurePlate", rrs.LightWeightedPressurePlate)
        self.globals.set("HeavyWeightedPressurePlate", rrs.HeavyWeightedPressurePlate)
        self.globals.set("Dirt", rrs.Dirt)
        self.globals.set("GrassBlock", rrs.GrassBlock)
        self.globals.set("Podzol", rrs.Podzol)
        self.globals.set("Cobblestone", rrs.Cobblestone)
        self.globals.set("OakPlanks", rrs.OakPlanks)
        self.globals.set("SprucePlanks", rrs.SprucePlanks)
        self.globals.set("BirchPlanks", rrs.BirchPlanks)
        self.globals.set("JunglePlanks", rrs.JunglePlanks)
        self.globals.set("AcaciaPlanks", rrs.AcaciaPlanks)
        self.globals.set("DarkOakPlanks", rrs.DarkOakPlanks)
        self.globals.set("MangrovePlanks", rrs.MangrovePlanks)
        self.globals.set("CherryPlanks", rrs.CherryPlanks)
        self.globals.set("BambooPlanks", rrs.BambooPlanks)
        self.globals.set("Sand", rrs.Sand)
        self.globals.set("RedSand", rrs.RedSand)
        self.globals.set("Gravel", rrs.Gravel)
        self.globals.set("Glass", rrs.Glass)
        self.globals.set("TintedGlass", rrs.TintedGlass)
        self.globals.set("SlimeBlock", rrs.SlimeBlock)
        self.globals.set("HoneyBlock", rrs.HoneyBlock)
        self.globals.set("Terracotta", rrs.Terracotta)
        self.globals.set("WhiteConcrete", rrs.WhiteConcrete)
        self.globals.set("OrangeConcrete", rrs.OrangeConcrete)
        self.globals.set("MagentaConcrete", rrs.MagentaConcrete)
        self.globals.set("LightBlueConcrete", rrs.LightBlueConcrete)
        self.globals.set("YellowConcrete", rrs.YellowConcrete)
        self.globals.set("LimeConcrete", rrs.LimeConcrete)
        self.globals.set("PinkConcrete", rrs.PinkConcrete)
        self.globals.set("GrayConcrete", rrs.GrayConcrete)
        self.globals.set("LightGrayConcrete", rrs.LightGrayConcrete)
        self.globals.set("CyanConcrete", rrs.CyanConcrete)
        self.globals.set("PurpleConcrete", rrs.PurpleConcrete)
        self.globals.set("BlueConcrete", rrs.BlueConcrete)
        self.globals.set("BrownConcrete", rrs.BrownConcrete)
        self.globals.set("GreenConcrete", rrs.GreenConcrete)
        self.globals.set("RedConcrete", rrs.RedConcrete)
        self.globals.set("BlackConcrete", rrs.BlackConcrete)
        self.globals.set("WhiteTerracotta", rrs.WhiteTerracotta)
        self.globals.set("OrangeTerracotta", rrs.OrangeTerracotta)
        self.globals.set("MagentaTerracotta", rrs.MagentaTerracotta)
        self.globals.set("LightBlueTerracotta", rrs.LightBlueTerracotta)
        self.globals.set("YellowTerracotta", rrs.YellowTerracotta)
        self.globals.set("LimeTerracotta", rrs.LimeTerracotta)
        self.globals.set("PinkTerracotta", rrs.PinkTerracotta)
        self.globals.set("GrayTerracotta", rrs.GrayTerracotta)
        self.globals.set("LightGrayTerracotta", rrs.LightGrayTerracotta)
        self.globals.set("CyanTerracotta", rrs.CyanTerracotta)
        self.globals.set("PurpleTerracotta", rrs.PurpleTerracotta)
        self.globals.set("BlueTerracotta", rrs.BlueTerracotta)
        self.globals.set("BrownTerracotta", rrs.BrownTerracotta)
        self.globals.set("GreenTerracotta", rrs.GreenTerracotta)
        self.globals.set("RedTerracotta", rrs.RedTerracotta)
        self.globals.set("BlackTerracotta", rrs.BlackTerracotta)
        self.globals.set("WhiteStainedGlass", rrs.WhiteStainedGlass)
        self.globals.set("OrangeStainedGlass", rrs.OrangeStainedGlass)
        self.globals.set("MagentaStainedGlass", rrs.MagentaStainedGlass)
        self.globals.set("LightBlueStainedGlass", rrs.LightBlueStainedGlass)
        self.globals.set("YellowStainedGlass", rrs.YellowStainedGlass)
        self.globals.set("LimeStainedGlass", rrs.LimeStainedGlass)
        self.globals.set("PinkStainedGlass", rrs.PinkStainedGlass)
        self.globals.set("GrayStainedGlass", rrs.GrayStainedGlass)
        self.globals.set("LightGrayStainedGlass", rrs.LightGrayStainedGlass)
        self.globals.set("CyanStainedGlass", rrs.CyanStainedGlass)
        self.globals.set("PurpleStainedGlass", rrs.PurpleStainedGlass)
        self.globals.set("BlueStainedGlass", rrs.BlueStainedGlass)
        self.globals.set("BrownStainedGlass", rrs.BrownStainedGlass)
        self.globals.set("GreenStainedGlass", rrs.GreenStainedGlass)
        self.globals.set("RedStainedGlass", rrs.RedStainedGlass)
        self.globals.set("BlackStainedGlass", rrs.BlackStainedGlass)
        self.globals.set("PoweredRail", rrs.PoweredRail)
        self.globals.set("DetectorRail", rrs.DetectorRail)
        self.globals.set("ActivatorRail", rrs.ActivatorRail)
        self.globals.set("Rail", rrs.Rail)
        self.globals.set("Lectern", rrs.Lectern)
        self.globals.set("WhiteGlazedTerracotta", rrs.WhiteGlazedTerracotta)
        self.globals.set("OrangeGlazedTerracotta", rrs.OrangeGlazedTerracotta)
        self.globals.set("MagentaGlazedTerracotta", rrs.MagentaGlazedTerracotta)
        self.globals.set("LightBlueGlazedTerracotta", rrs.LightBlueGlazedTerracotta)
        self.globals.set("YellowGlazedTerracotta", rrs.YellowGlazedTerracotta)
        self.globals.set("LimeGlazedTerracotta", rrs.LimeGlazedTerracotta)
        self.globals.set("PinkGlazedTerracotta", rrs.PinkGlazedTerracotta)
        self.globals.set("GrayGlazedTerracotta", rrs.GrayGlazedTerracotta)
        self.globals.set("LightGrayGlazedTerracotta", rrs.LightGrayGlazedTerracotta)
        self.globals.set("CyanGlazedTerracotta", rrs.CyanGlazedTerracotta)
        self.globals.set("PurpleGlazedTerracotta", rrs.PurpleGlazedTerracotta)
        self.globals.set("BlueGlazedTerracotta", rrs.BlueGlazedTerracotta)
        self.globals.set("BrownGlazedTerracotta", rrs.BrownGlazedTerracotta)
        self.globals.set("GreenGlazedTerracotta", rrs.GreenGlazedTerracotta)
        self.globals.set("RedGlazedTerracotta", rrs.RedGlazedTerracotta)
        self.globals.set("BlackGlazedTerracotta", rrs.BlackGlazedTerracotta)
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
