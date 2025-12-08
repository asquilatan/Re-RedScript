import os
from lark import Lark, Transformer, v_args
from lark.indenter import Indenter as LarkIndenter
from .ast import (
    Program, ModuleDef, FunctionCall, Arg, Kwarg,
    Literal, Variable, BinaryOp, TupleExpr, Statement
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
        # Items: "module" (token), CNAME, params (optional), suite
        # "module" is anonymous terminal -> it is in items? Yes.
        # But wait, "module" string literal is not named, so it might appear?
        # Actually, let's look at items.
        # If "module" is not named, it appears as a Token if not suppressed?
        # Anonymous terminals are usually filtered if they are string literals?
        # No, "module" matches the token but if it's not a named rule, it might just be consumed.
        # Let's inspect items safely.
        
        # We expect: CNAME, [params], suite
        # Because "module", _LPAR, _RPAR, _COLON are filtered.
        # But "module" is not filtered if it's just "module".
        # Let's assume items are: [Token('module'), CNAME, params?, suite]
        # Or [CNAME, params?, suite] if "module" is filtered.
        # Lark filters anonymous string literals by default? No.
        # But we can check.
        
        # Safe unpacking:
        # Filter out Tokens that match "module"
        clean_items = [x for x in items if not (hasattr(x, 'type') and x.type == 'MODULE')] # If I named it
        # Actually, simple check:
        # CNAME is definitely there. suite is definitely there.
        
        name = None
        params = []
        suite = None
        
        for item in items:
            if hasattr(item, 'type') and item.type == 'CNAME':
                name = str(item)
            elif isinstance(item, list) and len(item) > 0 and isinstance(item[0], str): 
                # params is list of strings
                params = item
            elif isinstance(item, list) and len(item) > 0 and isinstance(item[0], Statement):
                # suite is list of statements
                suite = item
            elif isinstance(item, list) and len(item) == 0:
                # empty params or empty suite (suite usually not empty)
                pass
        
        # Fallback if manual loop failed (e.g. params is None or empty list)
        # suite is the last item
        suite = items[-1]
        # name is the first CNAME
        # params is in between
        
        # Let's rely on position now that terminals are hidden
        # items: [Token(module), CNAME, params?, suite]
        # or [CNAME, params?, suite]
        
        idx = 0
        if isinstance(items[0], str) and items[0] == "module":
            idx += 1
        elif hasattr(items[0], 'type') and items[0].value == "module":
             idx += 1
             
        name = str(items[idx])
        idx += 1
        
        if idx < len(items) - 1:
            params = items[idx]
            idx += 1
        else:
            params = []
            
        suite = items[idx]
        
        return ModuleDef(name=name, params=params, body=suite)

    def params(self, items):
        # Items are CNAME tokens (COMMA is hidden)
        return [str(token) for token in items]

    def suite(self, items):
        # _NEWLINE _INDENT _DEDENT hidden? 
        # _NEWLINE is terminal. _INDENT/_DEDENT are special.
        # They should be hidden from transformer if they are terminals? 
        # No, they might appear.
        # But my rule `suite: statement+` (ignoring indent tokens in rule body?)
        # My rule: `suite: _NEWLINE _INDENT statement+ _DEDENT`
        # Hidden terminals are removed from items.
        # So items should contain only `statement+`.
        return items

    def instruction(self, items):
        return items[0]

    def function_call(self, items):
        # Items: CNAME, arguments?
        name = str(items[0])
        args = []
        kwargs = []
        
        if len(items) > 1:
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
        # CNAME _EQUALS expression -> CNAME, expression
        return Kwarg(name=str(items[0]), value=items[1])

    # Expressions
    def number(self, items):
        val = items[0]
        try:
            return Literal(value=int(val))
        except ValueError:
            return Literal(value=float(val))

    def string(self, items):
        return Literal(value=str(items[0])[1:-1]) # Remove quotes

    def var(self, items):
        return Variable(name=str(items[0]))
    
    def tuple(self, items):
         # _LPAR ... _RPAR hidden
         # items are expressions
         return TupleExpr(elements=items)

    def add(self, items): return BinaryOp(left=items[0], op='+', right=items[1])
    def sub(self, items): return BinaryOp(left=items[0], op='-', right=items[1])
    def mul(self, items): return BinaryOp(left=items[0], op='*', right=items[1])
    def div(self, items): return BinaryOp(left=items[0], op='/', right=items[1])

class RRSParser:
    def __init__(self):
        with open(GRAMMAR_PATH, 'r') as f:
            grammar = f.read()
        
        self.lark = Lark(grammar, parser='lalr', transformer=RRSTransformer(), postlex=Indenter())

    def parse(self, code: str) -> Program:
        return self.lark.parse(code)

    def parse_file(self, path: str) -> Program:
        with open(path, 'r') as f:
            content = f.read()
        return self.parse(content)

class Indenter(LarkIndenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['_LPAR']
    CLOSE_PAREN_types = ['_RPAR']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4