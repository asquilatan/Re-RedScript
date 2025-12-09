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
class ListExpr(Expr):
    elements: List[Expr]

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
class AssertStmt(Statement):
    test: Expr
    msg: Optional[Expr] = None

ASTNode = Node
