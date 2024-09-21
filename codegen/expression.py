"""Expression parser (for arr1, arr2, cond, and vercond xml attributes of
<add> tag)."""
import ast
import math
import operator

from .naming_conventions import name_access


class LiteralFloat(float):

    def __new__(cls, *args, **kwargs):
        return super(LiteralFloat, cls).__new__(cls, *args, **kwargs)

    def __str__(self):
        if self in (math.inf, -math.inf):
            return f"float('{super(LiteralFloat, LiteralFloat).__str__(self)}')"
        else:
            return super().__str__()


class Version(object):
    shifts = tuple(i for i in range(24, -1, -8))

    def __init__(self, expr_str: str):
        self.expr_str = expr_str
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

    def __str__(self):
        """Reconstruct the expression to a string."""
        if self.value is not None:
            return str(self.value)
        else:
            return ""


def interpret_literal(input_str, include_version=False):
    """interpret numeric values as written in the xml and return the unambiguous python equivalent (back-printable to their literals)"""
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


def str_is_number(str_expr):
    # check if it might be an int:
    return interpret_literal is None


def format_potential_tuple(value):
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

    operators = {'!': lambda a, b: not b,
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

    op_replacement = {'&&': 'and',
                      '||': 'or',
                      '!': 'not'}

    def __init__(self, expr_str, target_variable=""):
        try:
            left, self._op, right = self._partition(expr_str)
            self._left = self._parse(left, target_variable)
            self._right = self._parse(right, target_variable)
        except:
            print(f"error while parsing expression '{expr_str}'")
            raise

    def __str__(self):
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

    def __repr__(self):
        return str(self)

    @classmethod
    def _parse(cls, expr_str, target_variable=""):
        """Returns an Expression, string, or int, depending on the
        contents of <expr_str>."""
        if not expr_str:
            # empty string
            return None
        # try to convert it to one of the following classes
        literal_object = interpret_literal(expr_str, include_version=True)
        if literal_object is not None:
            return literal_object
        # brackets or operators => expression
        if ("(" in expr_str) or (")" in expr_str):
            return Expression(expr_str, target_variable)
        for op in cls.operators:
            if expr_str.find(op) != -1:
                return Expression(expr_str, target_variable)
        # at this point, expr_str is a single attribute
        # apply name filter on each component separately
        # (where a dot separates components)
        prefix = f"{target_variable}." if target_variable else ""
        return prefix + name_access(expr_str)

    @classmethod
    def _partition(cls, expr_str):
        """Partitions expr_str. See examples below.

        >>> Expression._partition('abc || efg')
        ('abc', '||', 'efg')
        >>> Expression._partition('(a== b) &&(( b!=c)||d )')
        ('a== b', '&&', '( b!=c)||d')
        >>> Expression._partition('!(1 <= 2)')
        ('', '!', '(1 <= 2)')
        >>> Expression._partition('')
        ('', '', '')
        """

        # strip whitespace
        expr_str = expr_str.strip()

        # all operators have a left hand side and a right hand side
        # except for negation, so let us deal with that case first
        if expr_str.startswith("!"):
            return "", "!", expr_str[1:].strip()

        # check if the left hand side starts with brackets
        # and if so, find the position of the starting bracket and the ending
        # bracket
        left_startpos, left_endpos = cls._scan_brackets(expr_str)
        if left_startpos == 0:
            # yes, it is a bracketted expression
            # so remove brackets and whitespace,
            # and let that be the left hand side
            left_str = expr_str[left_startpos + 1:left_endpos].strip()
            # if there is no next token, then just return the expression
            # without brackets
            if left_endpos + 1 == len(expr_str):
                return left_str, "", ""
            # the next token should be the operator
            # find the position where the operator should start
            op_startpos = left_endpos + 1
            while expr_str[op_startpos] == " ":
                op_startpos += 1
            # to avoid confusion between && and &, and || and |,
            # let's first scan for operators of two characters
            # and then for operators of one character
            for op_endpos in range(op_startpos + 1, op_startpos - 1, -1):
                op_str = expr_str[op_startpos:op_endpos + 1]
                if op_str in cls.operators:
                    break
            else:
                raise ValueError(f"expression syntax error: expected operator at '{expr_str[op_startpos:]}'")
        else:
            # it's not... so we need to scan for the first operator
            for op_startpos, ch in enumerate(expr_str):
                if ch == ' ': continue
                if ch == '(' or ch == ')':
                    raise ValueError(f"expression syntax error: expected operator before '{expr_str[op_startpos:]}'")
                # to avoid confusion between && and &, and || and |,
                # let's first scan for operators of two characters
                for op_endpos in range(op_startpos + 1, op_startpos - 1, -1):
                    op_str = expr_str[op_startpos:op_endpos + 1]
                    if op_str in cls.operators:
                        break
                else:
                    continue
                break
            else:
                # no operator found, so we are done
                left_str = expr_str.strip()
                op_str = ''
                right_str = ''
                return left_str, op_str, right_str
            # operator found! now get the left hand side
            left_str = expr_str[:op_startpos].strip()

        # now we have done the left hand side, and the operator
        # all that is left is to process the right hand side
        right_startpos, right_endpos = cls._scan_brackets(expr_str, op_endpos + 1)
        if right_startpos >= 0:
            # yes, we found a bracketted expression
            # so remove brackets and whitespace,
            # and let that be the right hand side
            right_str = expr_str[right_startpos + 1:right_endpos].strip()
            # check for trailing junk
            if expr_str[right_endpos + 1:] and not expr_str[right_endpos + 1:] == ' ':
                for op in cls.operators:
                    if expr_str.find(op) != -1:
                        break
                else:
                    raise ValueError(
                        f"expression syntax error: unexpected trailing characters '{expr_str[right_endpos + 1:]}'")
                # trailing characters contain an operator: do not remove
                # brackets but take
                # everything to be the right hand side (this happens for
                # instance in '(x <= y) && (y <= z) && (x != z)')
                right_str = expr_str[op_endpos + 1:].strip()
        else:
            # no, so just take the whole expression as right hand side
            right_str = expr_str[op_endpos + 1:].strip()
            # check that it is a valid expression
            if ("(" in right_str) or (")" in right_str):
                raise ValueError(f"expression syntax error: unexpected brackets in '{right_str}'")
        return left_str, op_str, right_str

    @staticmethod
    def _scan_brackets(expr_str, fromIndex=0):
        """Looks for matching brackets.

        >>> Expression._scan_brackets('abcde')
        (-1, -1)
        >>> Expression._scan_brackets('()')
        (0, 1)
        >>> Expression._scan_brackets('(abc(def))g')
        (0, 9)
        >>> s = '  (abc(dd efy 442))xxg'
        >>> start_pos, end_pos = Expression._scan_brackets(s)
        >>> print(s[start_pos+1:end_pos])
        abc(dd efy 442)
        """
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
    def eval_part(part, namespace):
        if isinstance(part, Expression):
            return part.eval(namespace)
        elif isinstance(part, str):
            return namespace[part.strip()]
        else:
            # use conversion to str to autoconvert Version to int
            return ast.literal_eval(str(part))

    def eval(self, namespace={}):
        left = self.eval_part(self._left, namespace)
        if not self._op:
            return left
        right = self.eval_part(self._right, namespace)
        return self.operators[self._op.strip()](left, right)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
