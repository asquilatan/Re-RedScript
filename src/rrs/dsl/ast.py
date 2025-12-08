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
class FunctionCall(Statement):
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