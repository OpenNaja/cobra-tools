"""Expression parser (for arr1, arr2, cond, and vercond xml attributes of
<add> tag)."""

from codegen import naming_conventions as convention


class Version(object):
    shifts = tuple(i for i in range(24, -1, -8))

    def __init__(self, expr_str: str):
        self.expr_str = expr_str
        # print(expr_str)
        if not expr_str:
            self.value = None
        else:
            byte_number_strs = expr_str.split(".")
            self.value = sum(int(n) << shift for n, shift in zip(byte_number_strs, self.shifts))
        # print(self)

    def version_number(version_str):
        """Converts version string into an integer.
        :param version_str: The version string.
        :type version_str: str
        :return: A version integer.
        >>> hex(NifFormat.version_number('3.14.15.29'))
        '0x30e0f1d'
        >>> hex(NifFormat.version_number('1.2'))
        '0x1020000'
        >>> hex(NifFormat.version_number('3.03'))
        '0x3000300'
        >>> hex(NifFormat.version_number('NS'))
        '0xa010000'
        """

        # 3.03 case is special
        if version_str == '3.03':
            return 0x03000300

        # NS (neosteam) case is special
        if version_str == 'NS':
            return 0x0A010000

        try:
            ver_list = [int(x) for x in version_str.split('.')]
        except ValueError:
            return -1 # version not supported (i.e. version_str '10.0.1.3a' would trigger this)
        if len(ver_list) > 4 or len(ver_list) < 1:
            return -1 # version not supported
        for ver_digit in ver_list:
            if (ver_digit | 0xff) > 0xff:
                return -1 # version not supported
        while len(ver_list) < 4: ver_list.append(0)
        return (ver_list[0] << 24) + (ver_list[1] << 16) + (ver_list[2] << 8) + ver_list[3]

    def __str__(self):
        """Reconstruct the expression to a string."""
        if self.value:
            return str(hex(self.value))
        else:
            return ""


class Expression(object):
    """This class represents an expression.

    >>> class A(object):
    ...     x = False
    ...     y = True
    >>> a = A()
    >>> e = Expression('x || y')
    >>> e.eval(a)
    1
    >>> Expression('99 & 15').eval(a)
    3
    >>> bool(Expression('(99&15)&&y').eval(a))
    True
    >>> a.hello_world = False
    >>> def nameFilter(s):
    ...     return 'hello_' + s.lower()
    >>> bool(Expression('(99 &15) &&WoRlD', name_filter = nameFilter).eval(a))
    False
    >>> Expression('c && d').eval(a)
    Traceback (most recent call last):
        ...
    AttributeError: 'A' object has no attribute 'c'
    >>> bool(Expression('1 == 1').eval())
    True
    >>> bool(Expression('(1 == 1)').eval())
    True
    >>> bool(Expression('1 != 1').eval())
    False
    """

    operators = {'==', '!=', '>=', '<=', '&&', '||', '&', '|', '-', '!', '<', '>', '/', '*', '+', '%'}

    def __init__(self, expr_str, name_filter=None):
        try:
            left, self._op, right = self._partition(expr_str)
            self._left = self._parse(left, name_filter)
            self._right = self._parse(right, name_filter)
        except:
            print("error while parsing expression '%s'" % expr_str)
            raise

    def eval(self, data=None):
        """Evaluate the expression to an integer."""

        if isinstance(self._left, Expression):
            left = self._left.eval(data)
        elif isinstance(self._left, str):
            if self._left == '""':
                left = ""
            else:
                left = data
                for part in self._left.split("."):
                    left = getattr(left, part)
        elif isinstance(self._left, type):
            left = isinstance(data, self._left)
        elif self._left is None:
            pass
        else:
            assert (isinstance(self._left, int))  # debug
            left = self._left

        if not self._op:
            return left

        if isinstance(self._right, Expression):
            right = self._right.eval(data)
        elif isinstance(self._right, str):
            if (not self._right) or self._right == '""':
                right = ""
            else:
                right = getattr(data, self._right)
        elif isinstance(self._right, type):
            right = isinstance(data, self._right)
        elif self._right is None:
            pass
        else:
            assert (isinstance(self._right, int))  # debug
            right = self._right

        if self._op == '==':
            return left == right
        elif self._op == '!=':
            return left != right
        elif self._op == '>=':
            return left >= right
        elif self._op == '<=':
            return left <= right
        elif self._op == '&&':
            return left and right
        elif self._op == '||':
            return left or right
        elif self._op == '&':
            return left & right
        elif self._op == '|':
            return left | right
        elif self._op == '-':
            return left - right
        elif self._op == '!':
            return not (right)
        elif self._op == '>':
            return left > right
        elif self._op == '<':
            return left < right
        elif self._op == '/':
            return left / right
        elif self._op == '*':
            return left * right
        elif self._op == '+':
            return left + right
        elif self._op == '%':
            return left % right
        else:
            raise NotImplementedError("expression syntax error: operator '" + self._op + "' not implemented")

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
        for k, v in (("&&", "and"), ("||", "or"), ("!", "not")):
            if op.strip() == k:
                op = v
        # since we need it for arrays, round to int
        if op == "/":
            return f"int({left} {op} {right})"
        return f"{left} {op} {right}".strip()

    @classmethod
    def _parse(cls, expr_str, name_filter=None):
        """Returns an Expression, string, or int, depending on the
        contents of <expr_str>."""
        if not expr_str:
            # empty string
            return None
        # brackets or operators => expression
        if ("(" in expr_str) or (")" in expr_str):
            return Expression(expr_str, name_filter)
        for op in cls.operators:
            if expr_str.find(op) != -1:
                return Expression(expr_str, name_filter)
        # try to convert it to one of the following classes
        for create_cls in (int, Version):
            try:
                return create_cls(expr_str)
            # failed
            except ValueError:
                pass
        # at this point, expr_str is a single attribute
        # apply name filter on each component separately
        # (where a dot separates components)
        if name_filter is None:
            def name_filter(x):
                return convention.name_attribute(x)
        prefix = "self."
        # globals are stored on the stream
        # it is only a global if the leftmost member has version in it
        # ie. general_info.ms2_version is not a global
        if "version" in expr_str.split(".")[0].lower():
            prefix = "stream."
        return prefix + ('.'.join(name_filter(comp) for comp in expr_str.split(".")))

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
                raise ValueError("expression syntax error: expected operator at '%s'" % expr_str[op_startpos:])
        else:
            # it's not... so we need to scan for the first operator
            for op_startpos, ch in enumerate(expr_str):
                if ch == ' ': continue
                if ch == '(' or ch == ')':
                    raise ValueError("expression syntax error: expected operator before '%s'" % expr_str[op_startpos:])
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
                        "expression syntax error: unexpected trailing characters '%s'" % expr_str[right_endpos + 1:])
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
                raise ValueError("expression syntax error: unexpected brackets in '%s'" % right_str)
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

    def map_(self, func):
        if isinstance(self._left, Expression):
            self._left.map_(func)
        else:
            self._left = func(self._left)
        if isinstance(self._right, Expression):
            self._right.map_(func)
        else:
            self._right = func(self._right)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
