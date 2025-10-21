import pytest
from codegen.expression import Expression, Version, interpret_literal

# Tests for the Version class
def test_version_init():
	assert Version("1").value == 1
	assert Version("0x10").value == 16
	assert Version("1.2.3.4").value == 16909060
	assert str(Version("1.2.3.4")) == "16909060"
	assert str(Version("16")) == "16"

# Tests for the interpret_literal function
@pytest.mark.parametrize("input_str, expected", [
	("123", 123),
	("0xFF", 255),
	("1.5", 1.5),
	("-10.0", -10.0),
	("some_string", None),
	("True", True),
	("False", False),
])
def test_interpret_literal(input_str, expected):
	result = interpret_literal(input_str)
	assert result == expected
	if isinstance(expected, float):
		assert isinstance(result, float)

# Tests for the Expression class
@pytest.mark.parametrize("expr_str, target_var, expected_str", [
	("a #ADD# b", "self", "self.a + self.b"),
	("c #SUB# 10", "self", "self.c - 10"),
	("d #MUL# e", "self", "self.d * self.e"),
	("f #DIV# 2", "self", "int(self.f / 2)"),
	("g #MOD# 3", "self", "self.g % 3"),
	("h #LSH# 1", "self", "self.h << 1"),
	("i #RSH# 2", "self", "self.i >> 2"),
	("j #BITAND# 0x0F", "self", "self.j & 15"),
	("k #BITOR# 1", "self", "self.k | 1"),
	("l #LT# m", "self", "self.l < self.m"),
	("n #GT# 100", "self", "self.n > 100"),
	("o #LTE# p", "self", "self.o <= self.p"),
	("q #GTE# 0", "self", "self.q >= 0"),
	("r #EQ# s", "self", "self.r == self.s"),
	("t #NEQ# u", "self", "self.t != self.u"),
	("v #AND# w", "self", "self.v and self.w"),
	("x #OR# y", "self", "self.x or self.y"),
	("(a #EQ# 10) #AND# (b #GT# 5)", "self", "(self.a == 10) and (self.b > 5)"),
	("!(a #EQ# b)", "self", "not (self.a == self.b)"),
	("#VER# #EQ# 18", "context", "context.version == 18"),
	("#ARG#\\some_field", "instance", "instance.arg.some_field"),
])
def test_expression_parsing_and_str(expr_str, target_var, expected_str):
	# This test also implicitly tests token replacement from the fixture
	# We manually replace tokens here since we are not using the full parser
	tokens = [
		("#ADD#", "+"), ("#SUB#", "-"), ("#MUL#", "*"), ("#DIV#", "/"), ("#MOD#", "%"),
		("#LSH#", "<<"), ("#RSH#", ">>"), ("#BITAND#", "&"), ("#BITOR#", "|"),
		("#LT#", "<"), ("#GT#", ">"), ("#LTE#", "<="), ("#GTE#", ">="),
		("#EQ#", "=="), ("#NEQ#", "!="), ("#AND#", "&&"), ("#OR#", "||"),
		("\\", "."), ("#VER#", "version"), ("#ARG#", "arg")
	]
	for token, replacement in tokens:
		expr_str = expr_str.replace(token, replacement)
	
	expr = Expression(expr_str, target_var)
	assert str(expr) == expected_str

def test_expression_evaluation():
	# Expanded namespace with more variables for complex tests
	namespace = {
		'a': 10, 
		'b': 20, 
		'v_true': True, 
		'v_false': False,
		'x': 5,
		'y': 3,
		'context.use_djb': True,
		'version': 10,
	}
	
	# --- Original Assertions ---
	assert Expression("a + b").eval(namespace) == 30
	assert Expression("b > a").eval(namespace) == True
	assert Expression("(a == 10) && v_true").eval(namespace) == True
	assert Expression("!v_true").eval(namespace) == False
	
	# --- New Arithmetic Assertions ---
	assert Expression("a * x").eval(namespace) == 50
	assert Expression("b / a").eval(namespace) == 2  # Should handle integer division
	assert Expression("a / y").eval(namespace) == 3  # 10 / 3 = 3 (integer division)
	assert Expression("a % y").eval(namespace) == 1  # 10 mod 3 = 1
	assert Expression("x * y + a").eval(namespace) == 25 # Test precedence: multiplication before addition
	assert Expression("a + 5").eval(namespace) == 15
	assert Expression("100 - b").eval(namespace) == 80

	assert Expression("!(a == 10) && v_true").eval(namespace) == False
	assert Expression("(a == 10) && !v_true").eval(namespace) == False
	assert Expression("!( (a == 10) && v_true )").eval(namespace) == False

	# Operator precedence (AND before OR)
	# (a == 10) && d || c   ->   (True && False) || True   ->   False || True   ->   True
	assert Expression("a == 10 && v_false || v_true").eval(namespace) == True

	# Overriding precedence with parentheses
	# a == 10 && (d || c)   ->   True && (False || True)   ->   True && True   ->   True
	assert Expression("a == 10 && (v_false || v_true)").eval(namespace) == True
	
	# More complex nesting
	assert Expression("! (a > b || (x < y && v_true))").eval(namespace) == True # ! (False || (False && True)) -> ! (False || False) -> !False -> True

	# --- New Bitwise Assertions ---
	assert Expression("a & x").eval(namespace) == 0   # 1010 & 0101 = 0000
	assert Expression("a | y").eval(namespace) == 11  # 1010 | 0011 = 1011
	assert Expression("x << 1").eval(namespace) == 10 # 0101 << 1 = 1010
	assert Expression("b >> 2").eval(namespace) == 5  # 10100 >> 2 = 00101
	
	assert Expression("((context.use_djb) && (version == 20))").eval(namespace) == False
	assert Expression("((context.use_djb) && (version == 10))").eval(namespace) == True
	assert Expression("((context.use_djb) && version == 10)").eval(namespace) == True
	assert Expression("(context.use_djb && version == 10)").eval(namespace) == True
	assert Expression("context.use_djb && version == 10").eval(namespace) == True

	# --- Assertions for Literal Fallback ---
	# These would have failed before
	assert Expression("v_true && True").eval(namespace) == True
	assert Expression("v_true && False").eval(namespace) == False
	assert Expression("v_true && v_true == True").eval(namespace) == True
	assert Expression("v_true && v_true == False").eval(namespace) == False
	assert Expression("False || v_false").eval(namespace) == False
	assert Expression("v_false || False").eval(namespace) == False
	assert Expression("v_true && v_false == False").eval(namespace) == True
