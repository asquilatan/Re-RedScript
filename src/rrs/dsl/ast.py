from dataclasses import dataclass, field
from typing import List, Union, Optional, Any

@dataclass
class Node:
    pass

# Expressions
@dataclass
class Expr(Node):
    pass

@dataclass
class Literal(Expr):
    value: Any

@dataclass
class Variable(Expr):
    name: str

@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str
    right: Expr

@dataclass
class TupleExpr(Expr):
    elements: List[Expr]

# Arguments
@dataclass
class Arg(Node):
    value: Expr

@dataclass
class Kwarg(Node):
    name: str
    value: Expr

# Statements
@dataclass
class Statement(Node):
    pass

@dataclass
class ExprStmt(Statement):
    expr: Expr

@dataclass
class FunctionCall(Expr):
    name: str
    args: List[Arg] = field(default_factory=list)
    kwargs: List[Kwarg] = field(default_factory=list)

@dataclass
class ModuleDef(Statement):
    name: str
    params: List[str]
    body: List[Statement]

@dataclass
class Program(Node):
    statements: List[Statement]

# New Nodes for Advanced Features

@dataclass
class Assignment(Statement):
    target: str
    value: Expr

@dataclass
class AugAssignment(Statement):
    target: str
    op: str
    value: Expr

@dataclass
class UnaryOp(Expr):
    op: str
    operand: Expr

@dataclass
class ListExpr(Expr):
    elements: List[Expr]

@dataclass
class DictExpr(Expr):
    # pairs is a list of (key_expr, value_expr) tuples
    pairs: List[tuple]

@dataclass
class ForLoop(Statement):
    target: str
    iterable: Expr
    body: List[Statement]

@dataclass
class FuncDef(Statement):
    name: str
    params: List[str]
    body: List[Statement]

@dataclass
class ReturnStmt(Statement):
    value: Optional[Expr]

@dataclass
class ImportStmt(Statement):
    module_name: str
    alias: Optional[str] = None

@dataclass
class FromImportStmt(Statement):
    module_name: str
    names: List[str]  # List of names to import

@dataclass
class MethodCall(Expr):
    obj: Expr
    method: str
    args: List[Arg] = field(default_factory=list)
    kwargs: List[Kwarg] = field(default_factory=list)

@dataclass
class GetAttr(Expr):
    obj: Expr
    attr: str

@dataclass
class SimulateStmt(Statement):
    """Simulate((module, ticks) => { ... })"""
    module_var: str  # Variable name for the module
    ticks: Optional[Expr]  # Number of ticks, None for infinite
    body: List[Statement]  # Statements inside the callback

@dataclass
class TriggerBlock(Statement):
    """trigger: ... block inside a module"""
    body: List[Statement]

@dataclass
class AssertStmt(Statement):
    test: Expr
    msg: Optional[Expr] = None

@dataclass
class IfStmt(Statement):
    """If/elif/else statement"""
    condition: Expr
    body: List[Statement]
    elif_clauses: List[tuple]  # List of (condition, body) tuples
    else_body: List[Statement] = None

@dataclass
class WhileLoop(Statement):
    """While loop"""
    condition: Expr
    body: List[Statement]

@dataclass
class IndexExpr(Expr):
    """List/dict indexing: arr[i]"""
    obj: Expr
    index: Expr

@dataclass
class IndexAssignment(Statement):
    """Index assignment: arr[i] = value"""
    obj: Expr
    index: Expr
    value: Expr

ASTNode = Node
