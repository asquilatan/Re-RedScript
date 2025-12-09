"""
Unit tests for control flow, list operations, and math functions.
"""

import pytest
from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter


class TestControlFlow:
    """Tests for if/elif/else and while loops."""
    
    def test_if_statement_true_branch(self):
        """Test that if statement executes true branch."""
        code = """
x = 10
result = 0
if x > 5:
    result = 1
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == 1
    
    def test_if_statement_false_branch(self):
        """Test that if statement skips when condition is false."""
        code = """
x = 3
result = 0
if x > 5:
    result = 1
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == 0
    
    def test_if_else_statement(self):
        """Test if-else branching."""
        code = """
x = 3
result = 0
if x > 5:
    result = 1
else:
    result = 2
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == 2
    
    def test_if_elif_else_statement(self):
        """Test if-elif-else chain."""
        code = """
x = 5
result = 0
if x > 10:
    result = 1
elif x > 3:
    result = 2
else:
    result = 3
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == 2
    
    def test_while_loop(self):
        """Test basic while loop."""
        code = """
i = 0
total = 0
while i < 5:
    total += 1
    i += 1
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("total") == 5
        assert interp.globals.get("i") == 5
    
    def test_while_loop_with_break_condition(self):
        """Test while loop terminates correctly."""
        code = """
count = 0
val = 100
while val > 1:
    val = val / 2
    count += 1
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        # 100 -> 50 -> 25 -> 12.5 -> 6.25 -> 3.125 -> 1.5625 -> 0.78125
        assert interp.globals.get("count") == 7


class TestListOperations:
    """Tests for list creation, indexing, and functions."""
    
    def test_empty_list_creation(self):
        """Test creating an empty list."""
        code = """
my_list = []
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("my_list") == []
    
    def test_list_with_elements(self):
        """Test creating a list with elements."""
        code = """
my_list = [1, 2, 3]
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("my_list") == [1, 2, 3]
    
    def test_list_indexing(self):
        """Test list indexing access."""
        code = """
my_list = [10, 20, 30]
first = my_list[0]
second = my_list[1]
third = my_list[2]
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("first") == 10
        assert interp.globals.get("second") == 20
        assert interp.globals.get("third") == 30
    
    def test_list_index_assignment(self):
        """Test list index assignment."""
        code = """
my_list = [1, 2, 3]
my_list[1] = 99
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("my_list") == [1, 99, 3]
    
    def test_list_append(self):
        """Test append function."""
        code = """
my_list = []
append(my_list, 1)
append(my_list, 2)
append(my_list, 3)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("my_list") == [1, 2, 3]
    
    def test_list_len(self):
        """Test len function."""
        code = """
my_list = [1, 2, 3, 4, 5]
size = len(my_list)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("size") == 5
    
    def test_list_pop(self):
        """Test pop function."""
        code = """
my_list = [1, 2, 3]
last = pop(my_list)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("last") == 3
        assert interp.globals.get("my_list") == [1, 2]
    
    def test_list_insert(self):
        """Test insert function."""
        code = """
my_list = [1, 3]
insert(my_list, 1, 2)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("my_list") == [1, 2, 3]


class TestMathFunctions:
    """Tests for math functions."""
    
    def test_sqrt(self):
        """Test sqrt function."""
        code = """
result = sqrt(16)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == 4.0
    
    def test_pow(self):
        """Test pow function."""
        code = """
result = pow(2, 3)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == 8.0
    
    def test_abs(self):
        """Test abs function."""
        code = """
result = abs(-5)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == 5
    
    def test_floor_ceil(self):
        """Test floor and ceil functions."""
        code = """
f = floor(3.7)
c = ceil(3.2)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("f") == 3
        assert interp.globals.get("c") == 4
    
    def test_min_max(self):
        """Test min and max functions."""
        code = """
minimum = min(5, 3, 8)
maximum = max(5, 3, 8)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("minimum") == 3
        assert interp.globals.get("maximum") == 8
    
    def test_round(self):
        """Test round function."""
        code = """
r1 = round(3.4)
r2 = round(3.6)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("r1") == 3
        assert interp.globals.get("r2") == 4
    
    def test_pi_constant(self):
        """Test PI constant."""
        code = """
result = PI
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        import math
        assert interp.globals.get("result") == math.pi


class TestTypeConversions:
    """Tests for type conversion functions."""
    
    def test_str_conversion(self):
        """Test str conversion."""
        code = """
result = str(42)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == "42"
    
    def test_int_conversion(self):
        """Test int conversion."""
        code = """
result = int(3.7)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == 3
    
    def test_float_conversion(self):
        """Test float conversion."""
        code = """
result = float(5)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("result") == 5.0
    
    def test_bool_conversion(self):
        """Test bool conversion."""
        code = """
t = bool(1)
f = bool(0)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("t") == True
        assert interp.globals.get("f") == False


class TestBooleanLiterals:
    """Tests for True, False, None literals."""
    
    def test_true_false(self):
        """Test boolean literals."""
        code = """
t = True
f = False
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("t") == True
        assert interp.globals.get("f") == False


class TestBooleanLogic:
    """Tests for complex boolean expressions (and, or, not)."""

    def test_and_operator(self):
        """Test 'and' operator."""
        code = """
t = True and True
f1 = True and False
f2 = False and True
f3 = False and False
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("t") == True
        assert interp.globals.get("f1") == False
        assert interp.globals.get("f2") == False
        assert interp.globals.get("f3") == False

    def test_or_operator(self):
        """Test 'or' operator."""
        code = """
t1 = True or True
t2 = True or False
t3 = False or True
f = False or False
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("t1") == True
        assert interp.globals.get("t2") == True
        assert interp.globals.get("t3") == True
        assert interp.globals.get("f") == False

    def test_not_operator(self):
        """Test 'not' operator."""
        code = """
f = not True
t = not False
inv = not (True and False)
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("f") == False
        assert interp.globals.get("t") == True
        assert interp.globals.get("inv") == True

    def test_complex_expression(self):
        """Test mixed operators and parentheses."""
        code = """
# (True or False) and (not False) -> True and True -> True
res1 = (True or False) and (not False)

# True and False or True -> False or True -> True (and has higher precedence)
res2 = True and False or True

# not True or True -> False or True -> True (not has highest precedence)
res3 = not True or True
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("res1") == True
        assert interp.globals.get("res2") == True
        assert interp.globals.get("res3") == True

    def test_not_variable_assignment(self):
        """Test 'not' on variable assignment."""
        code = """
x = True
y = not x
z = not y
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("y") == False
        assert interp.globals.get("z") == True

    def test_if_with_complex_condition(self):
        """Test if statement with complex boolean condition."""
        code = """
x = 10
y = 5
res = 0
if (x > 5 and y < 10) or x == 0:
    res = 1
"""
        parser = RRSParser()
        program = parser.parse(code)
        interp = Interpreter()
        interp.run(program)
        assert interp.globals.get("res") == 1

