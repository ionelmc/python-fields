from fields import Fields

from pytest import fixture
from pytest import raises


def test_factory():
    class T1(Fields.a.b.c(1).d(2)):
        pass

    t = T1(1, 2)
    assert repr(t) == "<T1(a=1, b=2, c=1, d=2)>"


def test_factory_all_defaults():
    class T2(Fields.a(0).b(1).c(2).d(3)):
        pass

    t = T2()
    assert repr(t) == "<T2(a=0, b=1, c=2, d=3)>"


def test_factory_no_required_after_defaults():
    raises(TypeError, getattr, Fields.a(0).b, 'c')


def test_factory_no_required_after_defaults_2():
    raises(TypeError, type, 'Broken', (Fields.a(0).b,), {})


def test_factory_t3():
    class T3(Fields.a):
        pass

    t = T3(1)
    assert repr(t) == "<T3(a=1)>"


def test_factory_empty_raise():
    raises(TypeError, type, "T5", (Fields,), {})


@fixture(scope="module")
def cmp_class(request):
    class CmpC(Fields.a.b):
        pass

    return CmpC


def test_equal(cmp_class):
    """
    Equal objects are detected as equal.
    """
    assert cmp_class(1, 2) == cmp_class(1, 2)
    assert not (cmp_class(1, 2) != cmp_class(1, 2))


def test_unequal_same_class(cmp_class):
    """
    Unequal objects of correct type are detected as unequal.
    """
    assert cmp_class(1, 2) != cmp_class(2, 1)
    assert not (cmp_class(1, 2) == cmp_class(2, 1))


def test_unequal_different_class(cmp_class):
    """
    Unequal objects of differnt type are detected even if their attributes
    match.
    """
    class NotCmpC(object):
        a = 1
        b = 2
    assert cmp_class(1, 2) != NotCmpC()
    assert not (cmp_class(1, 2) == NotCmpC())


def test_lt(cmp_class):
    """
    __lt__ compares objects as tuples of attribute values.
    """
    for a, b in [
        ((1, 2),  (2, 1)),
        ((1, 2),  (1, 3)),
        (("a", "b"), ("b", "a")),
    ]:
        assert cmp_class(*a) < cmp_class(*b)


def test_lt_unordable(cmp_class):
    """
    __lt__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (cmp_class(1, 2).__lt__(42))


def test_le(cmp_class):
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
        assert cmp_class(*a) <= cmp_class(*b)


def test_le_unordable(cmp_class):
    """
    __le__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (cmp_class(1, 2).__le__(42))


def test_gt(cmp_class):
    """
    __gt__ compares objects as tuples of attribute values.
    """
    for a, b in [
        ((2, 1), (1, 2)),
        ((1, 3), (1, 2)),
        (("b", "a"), ("a", "b")),
    ]:
        assert cmp_class(*a) > cmp_class(*b)


def test_gt_unordable(cmp_class):
    """
    __gt__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (cmp_class(1, 2).__gt__(42))


def test_ge(cmp_class):
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
        assert cmp_class(*a) >= cmp_class(*b)


def test_ge_unordable(cmp_class):
    """
    __ge__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (cmp_class(1, 2).__ge__(42))


def test_hash(cmp_class):
    """
    __hash__ returns different hashes for different values.
    """
    assert hash(cmp_class(1, 2)) != hash(cmp_class(1, 1))


#
#
#class TestWithInit(object):
#    def test_sets_attributes(self):
#        """
#        The attributes are initialized using the passed keywords.
#        """
#        obj = InitC(a=1, b=2)
#        assert 1 == obj.a
#        assert 2 == obj.b
#
#    def test_custom_init(self):
#        """
#        The class initializer is called too.
#        """
#        with pytest.raises(ValueError):
#            InitC(a=1, b=1)
#
#    def test_passes_args(self):
#        """
#        All positional parameters are passed to the original initializer.
#        """
#        @with_init(["a"])
#        class InitWithArg(object):
#            def __init__(self, arg):
#                self.arg = arg
#
#        obj = InitWithArg(42, a=1)
#        assert 42 == obj.arg
#        assert 1 == obj.a
#
#    def test_passes_remaining_kw(self):
#        """
#        Keyword arguments that aren't used for attributes are passed to the
#        original initializer.
#        """
#        @with_init(["a"])
#        class InitWithKWArg(object):
#            def __init__(self, kw_arg=None):
#                self.kw_arg = kw_arg
#
#        obj = InitWithKWArg(a=1, kw_arg=42)
#        assert 42 == obj.kw_arg
#        assert 1 == obj.a
#
#    def test_does_not_pass_attrs(self):
#        """
#        The attributes are removed from the keyword arguments before they are
#        passed to the original initializer.
#        """
#        @with_init(["a"])
#        class InitWithKWArgs(object):
#            def __init__(self, **kw):
#                assert "a" not in kw
#                assert "b" in kw
#        InitWithKWArgs(a=1, b=42)
#
#    def test_defaults(self):
#        """
#        If defaults are passed, they are used as fallback.
#        """
#        @with_init(["a", "b"], defaults={"b": 2})
#        class InitWithDefaults(object):
#            pass
#        obj = InitWithDefaults(a=1)
#        assert 2 == obj.b
#
#    def test_missing_arg(self):
#        """
#        Raises `ValueError` if a value isn't passed.
#        """
#        with pytest.raises(ValueError):
#            InitC(a=1)
#
#
#@attributes(["a", "b"], create_init=True)
#class MagicWithInitC(object):
#    pass
#
#
#@attributes(["a", "b"], create_init=False)
#class MagicWithoutInitC(object):
#    pass
#
#
#class TestAttributes(object):
#    def test_leaves_init_alone(self):
#        """
#        If *create_init* is `False`, leave __init__ alone.
#        """
#        obj = MagicWithoutInitC()
#        with pytest.raises(AttributeError):
#            obj.a
#        with pytest.raises(AttributeError):
#            obj.b
#
#    def test_wraps_init(self):
#        """
#        If *create_init* is `True`, build initializer.
#        """
#        obj = MagicWithInitC(a=1, b=2)
#        assert 1 == obj.a
#        assert 2 == obj.b
