import os
from lark import Lark, Transformer, v_args
from lark.indenter import Indenter as LarkIndenter
from .ast import (
    Program, ModuleDef, FunctionCall, Arg, Kwarg,
    Literal, Variable, BinaryOp, TupleExpr, Statement,
    Assignment, AugAssignment, ListExpr, ForLoop, FuncDef, ReturnStmt,
    ImportStmt, FromImportStmt, MethodCall, GetAttr, ExprStmt
)

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "rrs.lark")

class RRSTransformer(Transformer):
    def start(self, items):
        # Filter out tokens (like _NEWLINE) and keep only Statements
        statements = [i for i in items if isinstance(i, Statement)]
        return Program(statements=statements)

    def statement(self, items):
        return items[0]

    def module_def(self, items):
        # items: [Token(module), CNAME, params?, suite]
        # We rely on finding CNAME and suite
        
        name = None
        params = []
        suite = None
        
        for item in items:
            if hasattr(item, 'type') and item.type == 'CNAME':
                name = str(item)
                break
        
        # Params is list of strings (from params rule)
        # Suite is list of statements (from suite rule)
        
        for item in items:
            if isinstance(item, list):
                if len(item) > 0 and isinstance(item[0], str):
                    params = item
                elif len(item) > 0 and isinstance(item[0], Statement):
                    suite = item
                elif len(item) == 0:
                    # Empty params or empty suite
                    pass
        
        # Fallback for suite if it's the last item and wasn't caught
        if suite is None:
            suite = items[-1]
            
        return ModuleDef(name=name, params=params, body=suite)

    def func_def(self, items):
        # "def" CNAME params? suite
        # items: [CNAME, params?, suite]
        # "def", _LPAR, _RPAR, _COLON filtered
        
        name = str(items[0])
        params = []
        suite = None
        
        # Remaining items can be params (list of strings) or suite (list of statements)
        for item in items[1:]:
            if isinstance(item, list):
                if len(item) > 0 and isinstance(item[0], str):
                    params = item
                elif len(item) > 0 and isinstance(item[0], Statement):
                    suite = item
                elif len(item) == 0:
                    # Empty params or empty suite
                    # If it's params, it's empty list.
                    pass
        
        if suite is None:
            suite = items[-1]
            
        return FuncDef(name=name, params=params, body=suite)

    def for_loop(self, items):
        # "for" CNAME "in" expression _COLON suite
        # items: [CNAME, expr, suite]
        target = str(items[0])
        iterable = items[1]
        body = items[2]
        return ForLoop(target=target, iterable=iterable, body=body)

    def assignment(self, items):
        # CNAME _EQUALS expression _NEWLINE
        # items: [CNAME, expr]
        return Assignment(target=str(items[0]), value=items[1])

    def aug_assignment(self, items):
        # CNAME "+=" expression _NEWLINE
        return AugAssignment(target=str(items[0]), op='+=', value=items[1])

    def import_stmt(self, items):
        # "import" CNAME ["as" CNAME] _NEWLINE
        # items: [CNAME, CNAME?]
        module_name = str(items[0])
        alias = None
        if len(items) > 1 and items[1] is not None:
            alias = str(items[1])
        return ImportStmt(module_name=module_name, alias=alias)

    def from_import_stmt(self, items):
        # "from" CNAME "import" CNAME (_COMMA CNAME)* _NEWLINE
        # items: [CNAME, CNAME, CNAME...]
        module_name = str(items[0])
        names = []
        for item in items[1:]:
            names.append(str(item))
        return FromImportStmt(module_name=module_name, names=names)

    def return_stmt(self, items):
        # "return" [expression] _NEWLINE
        # items: [expression?]
        value = None
        if len(items) > 0:
             value = items[0]
        return ReturnStmt(value=value)

    def params(self, items):
        return [str(token) for token in items]

    def suite(self, items):
        return items

    def instruction(self, items):
        return ExprStmt(expr=items[0])

    def function_call(self, items):
        name = str(items[0])
        args = []
        kwargs = []
        
        if len(items) > 1 and items[1] is not None:
            args, kwargs = items[1]
            
        return FunctionCall(name=name, args=args, kwargs=kwargs)

    def arguments(self, items):
        args = []
        kwargs = []
        for item in items:
            if isinstance(item, Arg):
                args.append(item)
            elif isinstance(item, Kwarg):
                kwargs.append(item)
        return args, kwargs

    def positional_arg(self, items):
        return Arg(value=items[0])

    def keyword_arg(self, items):
        return Kwarg(name=str(items[0]), value=items[1])

    # Expressions
    def number(self, items):
        val = items[0]
        try:
            return Literal(value=int(val))
        except ValueError:
            return Literal(value=float(val))

    def string(self, items):
        return Literal(value=str(items[0])[1:-1])

    def var(self, items):
        return Variable(name=str(items[0]))
    
    def tuple(self, items):
         return TupleExpr(elements=items)
         
    def list_expr(self, items):
        return ListExpr(elements=items)

    def method_call(self, items):
        # atom "." CNAME _LPAR [arguments] _RPAR
        # items: [atom, CNAME, args?]
        # "." is anonymous but might be filtered if it's just punctuation?
        # Wait, "." is NOT starting with _.
        # But in `getattr` error: items = [Variable(name='obj'), Token('CNAME', 'attr')]
        # So "." IS filtered.
        
        obj = items[0]
        # items[1] is CNAME?
        # Let's check if items[1] is "." token?
        # Based on getattr error, items[1] is CNAME.
        
        method = str(items[1])
        args = []
        kwargs = []
        if len(items) > 2:
            args, kwargs = items[2]
        return MethodCall(obj=obj, method=method, args=args, kwargs=kwargs)

    def getattr(self, items):
        # atom "." CNAME
        # items: [atom, CNAME]
        obj = items[0]
        attr = str(items[1])
        return GetAttr(obj=obj, attr=attr)


    def add(self, items): return BinaryOp(left=items[0], op='+', right=items[1])
    def sub(self, items): return BinaryOp(left=items[0], op='-', right=items[1])
    def mul(self, items): return BinaryOp(left=items[0], op='*', right=items[1])
    def div(self, items): return BinaryOp(left=items[0], op='/', right=items[1])

class RRSParser:
    def __init__(self):
        with open(GRAMMAR_PATH, 'r') as f:
            grammar = f.read()
        
        # Removed transformer from here to apply it explicitly
        self.lark = Lark(grammar, parser='lalr', postlex=Indenter())

    def parse(self, code: str) -> Program:
        # Ensure code ends with newline (grammar requires it)
        if not code.endswith('\n'):
            code = code + '\n'
        tree = self.lark.parse(code)
        return RRSTransformer().transform(tree)

    def parse_file(self, path: str) -> Program:
        with open(path, 'r') as f:
            content = f.read()
        return self.parse(content)

class Indenter(LarkIndenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['_LPAR', '_LSQB']
    CLOSE_PAREN_types = ['_RPAR', '_RSQB']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4