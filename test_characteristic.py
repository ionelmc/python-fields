from __future__ import absolute_import, division, print_function

from unittest import TestCase

from characteristic import eq_attrs, repr_attrs


@eq_attrs(["a", "b"])
class EqC(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class EqAttrsTestCase(TestCase):
    def test_equal(self):
        """
        Equal objects are detected as equal.
        """
        self.assertTrue(EqC(1, 2) == EqC(1, 2))
        self.assertFalse(EqC(1, 2) != EqC(1, 2))

    def test_unequal_same_class(self):
        """
        Unequal objects of correct type are detected as unequal.
        """
        self.assertTrue(EqC(1, 2) != EqC(2, 1))
        self.assertFalse(EqC(1, 2) == EqC(2, 1))

    def test_unequal_different_class(self):
        """
        Unequal objects of differnt type are detected even if their attributes
        match.
        """
        class NotEqC(object):
            a = 1
            b = 2
        self.assertTrue(EqC(1, 2) != NotEqC())
        self.assertFalse(EqC(1, 2) == NotEqC())

    def test_lt(self):
        """
        __lt__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((1, 2),  (2, 1)),
            ((1, 2),  (1, 3)),
            (("a", "b"), ("b", "a")),
        ]:
            self.assertTrue(EqC(*a) < EqC(*b))

    def test_le(self):
        """
        __le__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((1, 2),  (2, 1)),
            ((1, 2),  (1, 3)),
            ((1, 1),  (1, 1)),
            (("a", "b"), ("b", "a")),
            (("a", "b"), ("a", "b")),
        ]:
            self.assertTrue(EqC(*a) <= EqC(*b))

    def test_gt(self):
        """
        __gt__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((2, 1), (1, 2)),
            ((1, 3), (1, 2)),
            (("b", "a"), ("a", "b")),
        ]:
            self.assertTrue(EqC(*a) > EqC(*b))

    def test_ge(self):
        """
        __ge__ compares objects as tupges of attribute values.
        """
        for a, b in [
            ((2, 1), (1, 2)),
            ((1, 3), (1, 2)),
            ((1, 1), (1, 1)),
            (("b", "a"), ("a", "b")),
            (("a", "b"), ("a", "b")),
        ]:
            self.assertTrue(EqC(*a) >= EqC(*b))


@repr_attrs(["a", "b"])
class ReprC(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class ReprAttrsTestCase(TestCase):
    def test_repr(self):
        """
        Test repr returns a sensible value.
        """
        self.assertEqual("<ReprC(a=1, b=2)>", repr(ReprC(1, 2)))
