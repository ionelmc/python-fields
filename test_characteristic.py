from __future__ import absolute_import, division, print_function

import pytest

from characteristic import (
    attributes,
    with_cmp,
    with_init,
    with_repr,
)


@with_cmp(["a", "b"])
class CmpC(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class TestWithCmp(object):
    def test_equal(self):
        """
        Equal objects are detected as equal.
        """
        assert CmpC(1, 2) == CmpC(1, 2)
        assert not (CmpC(1, 2) != CmpC(1, 2))

    def test_unequal_same_class(self):
        """
        Unequal objects of correct type are detected as unequal.
        """
        assert CmpC(1, 2) != CmpC(2, 1)
        assert not (CmpC(1, 2) == CmpC(2, 1))

    def test_unequal_different_class(self):
        """
        Unequal objects of differnt type are detected even if their attributes
        match.
        """
        class NotCmpC(object):
            a = 1
            b = 2
        assert CmpC(1, 2) != NotCmpC()
        assert not (CmpC(1, 2) == NotCmpC())

    def test_lt(self):
        """
        __lt__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((1, 2),  (2, 1)),
            ((1, 2),  (1, 3)),
            (("a", "b"), ("b", "a")),
        ]:
            assert CmpC(*a) < CmpC(*b)

    def test_lt_unordable(self):
        """
        __lt__ returns NotImplemented if classes differ.
        """
        assert NotImplemented == (CmpC(1, 2).__lt__(42))

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
            assert CmpC(*a) <= CmpC(*b)

    def test_le_unordable(self):
        """
        __le__ returns NotImplemented if classes differ.
        """
        assert NotImplemented == (CmpC(1, 2).__le__(42))

    def test_gt(self):
        """
        __gt__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((2, 1), (1, 2)),
            ((1, 3), (1, 2)),
            (("b", "a"), ("a", "b")),
        ]:
            assert CmpC(*a) > CmpC(*b)

    def test_gt_unordable(self):
        """
        __gt__ returns NotImplemented if classes differ.
        """
        assert NotImplemented == (CmpC(1, 2).__gt__(42))

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
            assert CmpC(*a) >= CmpC(*b)

    def test_ge_unordable(self):
        """
        __ge__ returns NotImplemented if classes differ.
        """
        assert NotImplemented == (CmpC(1, 2).__ge__(42))

    def test_hash(self):
        """
        __hash__ returns different hashes for different values.
        """
        assert hash(CmpC(1, 2)) != hash(CmpC(1, 1))


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

    def test_passes_args(self):
        """
        All positional parameters are passed to the original initializator.
        """
        @with_init(["a"])
        class InitWithArg(object):
            def __init__(self, arg):
                self.arg = arg

        obj = InitWithArg(42, a=1)
        assert 42 == obj.arg
        assert 1 == obj.a

    def test_passes_remaining_kw(self):
        """
        Keyword arguments that aren't used for attributes are passed to the
        original initializator.
        """
        @with_init(["a"])
        class InitWithKWArg(object):
            def __init__(self, kw_arg=None):
                self.kw_arg = kw_arg

        obj = InitWithKWArg(a=1, kw_arg=42)
        assert 42 == obj.kw_arg
        assert 1 == obj.a

    def test_defaults(self):
        """
        If defaults are passed, they are used as fallback.
        """
        @with_init(["a", "b"], defaults={"b": 2})
        class InitWithDefaults(object):
            pass
        obj = InitWithDefaults(a=1)
        assert 2 == obj.b

    def test_missing_arg(self):
        """
        Raises `ValueError` if a value isn't passed.
        """
        with pytest.raises(ValueError):
            InitC(a=1)


@attributes(["a", "b"], create_init=True)
class MagicWithInitC(object):
    pass


@attributes(["a", "b"], create_init=False)
class MagicWithoutInitC(object):
    pass


class TestAttributes(object):
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
