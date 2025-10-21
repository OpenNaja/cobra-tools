"""Expression parser (for arr1, arr2, cond, and vercond xml attributes of
<add> tag)."""
import ast
import math
import operator
from typing import Self, Callable, Any

from .naming_conventions import name_access


class LiteralFloat(float):

    def __new__(cls, *args, **kwargs) -> Self:
        return super(LiteralFloat, cls).__new__(cls, *args, **kwargs)

    def __str__(self) -> str:
        if self in (math.inf, -math.inf):
            return f"float('{super(LiteralFloat, LiteralFloat).__str__(self)}')"
        else:
            return super().__str__()


class Version(object):
    shifts: tuple[int, ...] = tuple(i for i in range(24, -1, -8))

    def __init__(self, expr_str: str) -> None:
        self.expr_str: str = expr_str
        # print(expr_str)
        if not expr_str:
            self.value = None
        else:
            if "." in expr_str:
                byte_number_strs = expr_str.split(".")
                self.value = sum(int(n) << shift for n, shift in zip(byte_number_strs, self.shifts))
            else:
                # use int(x, 0) to evaluate x as an int literal, allowing for non-decimal (e.g. hex) values to be read
                self.value = int(expr_str, 0)

    def __str__(self) -> str:
        """Reconstruct the expression to a string."""
        if self.value is not None:
            return str(self.value)
        else:
            return ""


def interpret_literal(input_str: str, include_version: bool = False) -> int | LiteralFloat | Version | None:
    """interpret numeric values as written in the xml and return the unambiguous python equivalent (back-printable to their literals)"""
    if input_str == 'True':
        return True
    if input_str == 'False':
        return False
    try:
        return int(input_str, 0)
    except ValueError:
        pass
    try:
        return LiteralFloat(input_str)
    except:
        pass
    if include_version:
        try:
            return Version(input_str)
        except:
            pass
    return None


def format_potential_tuple(value: str) -> str:
    """Converts xml attribute value lists to tuples if space is present and all
    comma-space-separated values can be converted to numbers, otherwise leaves it alone.
    :param value: the string that is the value of an attribute
    :return: original string if no space is present, or commas as separators
    and surrounding parentheses if whitespace is present.
    >>> format_potential_tuple('1.0')
    '1.0
    >>> format_potential_tuple('1.0, 1.0, 1.0')
    '(1.0, 1.0, 1.0)'"""
    if ', ' in value:
        interpreted_literals = [interpret_literal(potential_number) for potential_number in value.split(', ')]
        if all([interpreted is not None for interpreted in interpreted_literals]):
            return f"({', '.join([str(interpreted) for interpreted in interpreted_literals])})"
        else:
            return value
    else:
        return value


class Expression(object):
    # Define operator precedence, from lowest to highest.
    PRECEDENCE = [
        ('||',),
        ('&&',),
        ('|',),
        ('&',),
        ('==', '!='),
        ('>', '>=', '<', '<='),
        ('<<', '>>'),
        ('+', '-'),
        ('*', '/', '%'),
    ]

    # Reverse mapping for quick lookup of an operator's precedence level
    OP_TO_PRECEDENCE = {
        op: i for i, ops in enumerate(PRECEDENCE) for op in ops
    }

    operators: dict[str, Callable[[Any, Any], Any]] = {'!': lambda a, b: not b,
                 '*': operator.mul,
                 '/': lambda a, b: int(operator.truediv(a, b)),
                 '%': operator.mod,
                 '+': operator.add,
                 '-': operator.sub,
                 '<<': operator.lshift,
                 '>>': operator.rshift,
                 '&': operator.and_,
                 '|': operator.or_,
                 '==': operator.eq,
                 '!=': operator.ne,
                 '>': operator.gt,
                 '>=': operator.ge,
                 '<': operator.lt,
                 '<=': operator.le,
                 '&&': lambda a, b: a and b,
                 '||': lambda a, b: a or b}
    
    op_replacement: dict[str, str] = {'&&': 'and', '||': 'or', '!': 'not'}

    def __init__(self, expr_str: str, target_variable: str = "") -> None:
        try:
            left, self._op, right = self._partition(expr_str)
            self._left = self._parse(left, target_variable)
            self._right = self._parse(right, target_variable)
        except:
            print(f"error while parsing expression '{expr_str}'")
            raise

    def __str__(self) -> str:
        """Reconstruct the expression to a string."""

        left = str(self._left) if self._left is not None else ""
        if not self._op:
            return left
        right = str(self._right) if self._right is not None else ""
        if isinstance(self._left, Expression):
            left = f"({left})"
        if isinstance(self._right, Expression):
            right = f"({right})"
        op = self._op
        op = self.op_replacement.get(op.strip(), op)
        # since we need it for arrays, round to int
        if op.strip() == "/":
            return f"int({left} {op} {right})"
        return f"{left} {op} {right}".strip()

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def _parse(cls, expr_str: str, target_variable: str = "") -> Any:
        if not expr_str:
            return None
        literal_object = interpret_literal(expr_str, include_version=True)
        if literal_object is not None:
            return literal_object
        
        # Check if the expression is fully enclosed in parentheses
        if expr_str.startswith('(') and expr_str.endswith(')'):
            start_pos, end_pos = cls._scan_brackets(expr_str)
            if start_pos == 0 and end_pos == len(expr_str) - 1:
                inner_content = expr_str[1:-1]
                has_binary_operator_inside = any(
                    op in inner_content for op in cls.operators if op != '!'
                )
                if not has_binary_operator_inside:
                    # Recursively parse the unwrapped content to handle nested
                    # redundant parentheses like ((a.b))
                    return cls._parse(inner_content, target_variable)
                return Expression(inner_content, target_variable)

        for op in cls.operators:
            if expr_str.find(op) != -1:
                return Expression(expr_str, target_variable)

        prefix = f"{target_variable}." if target_variable else ""
        return prefix + name_access(expr_str)

    @classmethod
    def _partition(cls, expr_str: str) -> tuple[str, str, str]:
        expr_str = expr_str.strip()

        if expr_str.startswith("!"):
            return "", "!", expr_str[1:].strip()

        if expr_str.startswith('(') and expr_str.endswith(')'):
            start_pos, end_pos = cls._scan_brackets(expr_str)
            if start_pos == 0 and end_pos == len(expr_str) - 1:
                return expr_str[1:-1].strip(), "", ""

        paren_depth = 0
        split_pos = -1
        # Initialize with a high value
        split_prec = float('inf')

        i = len(expr_str) - 1
        while i >= 0:
            char = expr_str[i]
            if char == ')':
                paren_depth += 1
            elif char == '(':
                paren_depth -= 1
            
            if paren_depth == 0:
                op_candidate = None
                # Check for 2-char operators
                if i > 0 and expr_str[i-1:i+1] in cls.OP_TO_PRECEDENCE:
                    op_candidate = expr_str[i-1:i+1]
                # Check for 1-char operators
                elif char in cls.OP_TO_PRECEDENCE:
                    op_candidate = char

                if op_candidate:
                    prec = cls.OP_TO_PRECEDENCE[op_candidate]
                    # Find the lowest precedence operator.
                    # The '<=' handles left-to-right associativity
                    # by selecting the right-most operator of the same lowest precedence.
                    if prec <= split_prec:
                        split_prec = prec
                        split_pos = i - (len(op_candidate) - 1)
            i -= 1
            
        if split_pos != -1:
            op_len = 2 if expr_str[split_pos:split_pos+2] in cls.operators else 1
            op = expr_str[split_pos : split_pos + op_len]

            left = expr_str[:split_pos].strip()
            right = expr_str[split_pos + len(op):].strip()
            return left, op, right

        return expr_str, "", ""

    @staticmethod
    def _scan_brackets(expr_str: str, fromIndex: int = 0) -> tuple[int, int]:
        start_pos = -1
        end_pos = -1
        scan_depth = 0
        for scan_pos in range(fromIndex, len(expr_str)):
            scan_char = expr_str[scan_pos]
            if scan_char == "(":
                if start_pos == -1:
                    start_pos = scan_pos
                scan_depth += 1
            elif scan_char == ")":
                scan_depth -= 1
                if scan_depth == 0:
                    end_pos = scan_pos
                    break
        else:
            if start_pos != -1 or end_pos != -1:
                raise ValueError("expression syntax error (non-matching brackets?)")
        return start_pos, end_pos

    @staticmethod
    def eval_part(part: Any, namespace: dict[str, Any]) -> Any:
        if isinstance(part, Expression):
            return part.eval(namespace)
        elif isinstance(part, str):
            part = part.strip()
            if part in namespace:
                return namespace[part]
            else:
                return ast.literal_eval(part)
        else:
            return ast.literal_eval(str(part))

    def eval(self, namespace: dict[str, Any] = {}) -> Any:
        left = self.eval_part(self._left, namespace)
        if not self._op:
            return left
        right = self.eval_part(self._right, namespace)
        return self.operators[self._op.strip()](left, right)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
