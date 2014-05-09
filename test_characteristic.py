from __future__ import absolute_import, division, print_function

import pytest

from characteristic import (
    with_attributes,
    with_cmp,
    with_init,
    with_repr,
)


@with_cmp(["a", "b"])
class EqC(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class TestWithCmp(object):
    def test_equal(self):
        """
        Equal objects are detected as equal.
        """
        assert EqC(1, 2) == EqC(1, 2)
        assert not (EqC(1, 2) != EqC(1, 2))

    def test_unequal_same_class(self):
        """
        Unequal objects of correct type are detected as unequal.
        """
        assert EqC(1, 2) != EqC(2, 1)
        assert not (EqC(1, 2) == EqC(2, 1))

    def test_unequal_different_class(self):
        """
        Unequal objects of differnt type are detected even if their attributes
        match.
        """
        class NotEqC(object):
            a = 1
            b = 2
        assert EqC(1, 2) != NotEqC()
        assert not (EqC(1, 2) == NotEqC())

    def test_lt(self):
        """
        __lt__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((1, 2),  (2, 1)),
            ((1, 2),  (1, 3)),
            (("a", "b"), ("b", "a")),
        ]:
            assert EqC(*a) < EqC(*b)

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
            assert EqC(*a) <= EqC(*b)

    def test_gt(self):
        """
        __gt__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((2, 1), (1, 2)),
            ((1, 3), (1, 2)),
            (("b", "a"), ("a", "b")),
        ]:
            assert EqC(*a) > EqC(*b)

    def test_ge(self):
        """
        __ge__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((2, 1), (1, 2)),
            ((1, 3), (1, 2)),
            ((1, 1), (1, 1)),
            (("b", "a"), ("a", "b")),
            (("a", "b"), ("a", "b")),
        ]:
            assert EqC(*a) >= EqC(*b)

    def test_hash(self):
        """
        __hash__ returns different hashes for different values.
        """
        assert hash(EqC(1, 2)) != hash(EqC(1, 1))


@with_repr(["a", "b"])
class ReprC(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class TestReprAttrs(object):
    def test_repr(self):
        """
        Test repr returns a sensible value.
        """
        assert "<ReprC(a=1, b=2)>" == repr(ReprC(1, 2))


@with_init(["a", "b"])
class InitC(object):
    def __init__(self):
        if self.a == self.b:
            raise ValueError


class TestWithInit(object):
    def test_sets_attributes(self):
        """
        The attributes are initialized using the passed keywords.
        """
        obj = InitC(a=1, b=2)
        assert 1 == obj.a
        assert 2 == obj.b

    def test_custom_init(self):
        """
        The class initializator is called too.
        """
        with pytest.raises(ValueError):
            InitC(a=1, b=1)


@with_attributes(["a", "b"], create_init=True)
class MagicWithInitC(object):
    pass


@with_attributes(["a", "b"], create_init=False)
class MagicWithoutInitC(object):
    pass


class TestWithAttributes(object):
    def test_leaves_init_alone(self):
        """
        If *create_init* is `False`, leave __init__ alone.
        """
        obj = MagicWithoutInitC()
        with pytest.raises(AttributeError):
            obj.a
        with pytest.raises(AttributeError):
            obj.b

    def test_wraps_init(self):
        """
        If *create_init* is `True`, build initializer.
        """
        obj = MagicWithInitC(a=1, b=2)
        assert 1 == obj.a
        assert 2 == obj.b
