"""Expression parser (for arr1, arr2, cond, and vercond xml attributes of
<add> tag)."""

from codegen.naming_conventions import name_access


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
                # print(self)

    def version_number(version_str):
        """Converts version string into an integer.
        :param version_str: The version string.
        :type version_str: str
        :return: A version integer.
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
            return -1  # version not supported (i.e. version_str '10.0.1.3a' would trigger this)
        if len(ver_list) > 4 or len(ver_list) < 1:
            return -1  # version not supported
        for ver_digit in ver_list:
            if (ver_digit | 0xff) > 0xff:
                return -1  # version not supported
        while len(ver_list) < 4:
            ver_list.append(0)
        return (ver_list[0] << 24) + (ver_list[1] << 16) + (ver_list[2] << 8) + ver_list[3]

    def __str__(self):
        """Reconstruct tfhe expression to a string."""
        if self.value is not None:
            return str(self.value)
        else:
            return ""


class Expression(object):

    operators = {'==', '!=', '>=', '<=', '&&', '||', '&', '|', '-', '!', '<', '>', '/', '*', '+', '%'}

    def __init__(self, expr_str, attribute_prefix=""):
        try:
            left, self._op, right = self._partition(expr_str)
            self._left = self._parse(left, attribute_prefix)
            self._right = self._parse(right, attribute_prefix)
        except:
            print("error while parsing expression '%s'" % expr_str)
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
        for k, v in (("&&", "and"), ("||", "or"), ("!", "not")):
            if op.strip() == k:
                op = v
        # since we need it for arrays, round to int
        if op == "/":
            return f"int({left} {op} {right})"
        return f"{left} {op} {right}".strip()

    @classmethod
    def _parse(cls, expr_str, prefix=""):
        """Returns an Expression, string, or int, depending on the
        contents of <expr_str>."""
        if not expr_str:
            # empty string
            return None
        # brackets or operators => expression
        if ("(" in expr_str) or (")" in expr_str):
            return Expression(expr_str, prefix)
        for op in cls.operators:
            if expr_str.find(op) != -1:
                return Expression(expr_str, prefix)
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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
