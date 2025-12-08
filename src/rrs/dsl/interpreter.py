import rrs
from rrs.core.module import Module
from rrs.dsl.ast import Program, ModuleDef, FunctionCall, Literal, Variable, BinaryOp, TupleExpr
from typing import Dict, Any, List

class SymbolTable:
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
    def __init__(self):
        self.globals = SymbolTable()
        self.register_builtins()
        self.current_module: Module = None 
        self.modules_registry = {} 

    def register_builtins(self):
        self.globals.set("Piston", rrs.Piston)
        self.globals.set("Repeater", rrs.Repeater)
        self.globals.set("Stone", rrs.Stone)
        # We can add a mechanism to auto-discover blocks from rrs module

    def run(self, program: Program) -> List[Module]:
        # Pass 1: Register ModuleDefs
        for stmt in program.statements:
            if isinstance(stmt, ModuleDef):
                self.modules_registry[stmt.name] = stmt
        
        results = []
        # Pass 2: Execute top-level calls
        for stmt in program.statements:
            if isinstance(stmt, FunctionCall):
                res = self.visit_function_call(stmt, self.globals)
                if isinstance(res, Module):
                    results.append(res)
        
        return results

    def execute_module(self, name: str, args: List[Any], kwargs: Dict[str, Any]) -> Module:
        if name not in self.modules_registry:
            raise ValueError(f"Unknown module: {name}")
            
        def_node = self.modules_registry[name]
        
        if len(args) != len(def_node.params):
             raise ValueError(f"Module {name} expects {len(def_node.params)} args, got {len(args)}")
             
        scope = SymbolTable(parent=self.globals)
        for param, val in zip(def_node.params, args):
            scope.set(param, val)
            
        pos = kwargs.get('pos', (0,0,0))
        module_instance = Module(name, pos=pos)
        
        prev_module = self.current_module
        self.current_module = module_instance
        
        try:
            for stmt in def_node.body:
                if isinstance(stmt, FunctionCall):
                    child = self.visit_function_call(stmt, scope)
                    if isinstance(child, Module):
                         module_instance.add(child)
        finally:
            self.current_module = prev_module
            
        return module_instance

    def visit_function_call(self, node: FunctionCall, scope: SymbolTable):
        obj = scope.get(node.name)
        
        eval_args = [self.evaluate(arg.value, scope) for arg in node.args]
        eval_kwargs = {kw.name: self.evaluate(kw.value, scope) for kw in node.kwargs}
        
        if obj:
            # Builtin Block class
            instance = obj(*eval_args, **eval_kwargs)
            return instance
        elif node.name in self.modules_registry:
            # User defined module
            return self.execute_module(node.name, eval_args, eval_kwargs)
        else:
            raise ValueError(f"Unknown function/module: {node.name}")

    def evaluate(self, expr, scope: SymbolTable):
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Variable):
            val = scope.get(expr.name)
            if val is None:
                 raise ValueError(f"Undefined variable: {expr.name}")
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
        return None