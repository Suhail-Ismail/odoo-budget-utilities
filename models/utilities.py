# -*- coding: utf-8 -*-
import math
from math import log10, floor


def num_to_shorthand(num, ends=None):
    """
    Converts Number to short human readable numbers 
    """
    if ends is None:
        ends = ["", "K", "M", "B", "T"]

    num = int(num)
    str_num = str(num)
    index = int(floor(log10(num)) / 3)
    letter = ends[index]

    digit = str_num[0:len(str_num) - index * 3]

    return '{}{}'.format(digit, letter)


def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    '''
    Python 2 implementation of Python 3.5 math.isclose()
    https://hg.python.org/cpython/file/tip/Modules/mathmodule.c#l1993
    '''
    # sanity check on the inputs
    if rel_tol < 0 or abs_tol < 0:
        raise ValueError("tolerances must be non-negative")

    # short circuit exact equality -- needed to catch two infinities of
    # the same sign. And perhaps speeds things up a bit sometimes.
    if a == b:
        return True

    # This catches the case of two infinities of opposite sign, or
    # one infinity and one finite number. Two infinities of opposite
    # sign would otherwise have an infinite relative tolerance.
    # Two infinities of the same sign are caught by the equality check
    # above.
    if math.isinf(a) or math.isinf(b):
        return False

    # main comparator
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def choices_tuple(choices, is_sorted=True):
    choices = [(i.lower(), i.upper()) for i in choices]

    if is_sorted:
        return sorted(choices, key=lambda tup: tup[0])

    return choices


def odoo_to_pandas_list(orm_query=None, columns=list()):
    """
    Convert odoo query to list if dictionary readabloe to pandas   
    """
    columns = columns if columns else orm_query.fields_get_keys()
    data = []
    for row in orm_query:
        row_data = {}
        for column in columns:
            row_data[column] = row.mapped(column)[0]
        data.append(row_data)
    return data

def int_to_roman(input):
    """ Convert an integer to a Roman numeral. """

    if not isinstance(input, int):
        raise TypeError("expected integer, got %s" % type(input))
    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)


import unittest


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        numbers = [
            (1, '1'),
            (1.0, '1'),
            (11, '11'),
            (11.35223, '11'),
            (111, '111'),
            (1111, '1K'),
            (11111, '11K'),
            (111111, '111K'),
            (1111111, '1M'),
        ]

        for num in numbers:
            self.assertEqual(num_to_shorthand(num[0]), num[1])


if __name__ == '__main__':
    unittest.main()
