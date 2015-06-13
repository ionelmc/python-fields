from __future__ import print_function

import pickle
try:
    import cPickle
except ImportError:
    import pickle as cPickle
from functools import partial
from itertools import chain

from pytest import fixture
from pytest import raises

from fields import BareFields
from fields import ComparableMixin
from fields import ConvertibleFields
from fields import ConvertibleMixin
from fields import Fields
from fields import PrintableMixin
from fields import SlotsFields
from fields import Tuple
from fields.extras import RegexValidate
from fields.extras import ValidationError


@fixture(params=[
    partial(pickle.dumps, protocol=i)
    for i in range(pickle.HIGHEST_PROTOCOL)
] + [
    partial(cPickle.dumps, protocol=i)
    for i in range(cPickle.HIGHEST_PROTOCOL)
])
def pickler(request):
    return request.param


@fixture(params=[pickle.loads, cPickle.loads])
def unpickler(request):
    return request.param


@fixture(params=[Fields, SlotsFields])
def impl(request):
    print(request.param)
    return request.param


class G1(Tuple.a.b):
    pass


class G2(Fields.a.b[1].c[2]):
    pass


class G3(Fields.a.b[1].c[2]):
    pass


def test_slots_class_has_slots():
    class Slots(SlotsFields.a.b[1]):
        pass

    i = Slots(0)
    i.a = 1
    assert Slots.__slots__ == ['a', 'b']
    assert i.a == 1
    assert not hasattr(i, "__dict__")
    raises(AttributeError, setattr, i, "bogus", 1)
    raises(AttributeError, getattr, i, "bogus")


def test_slots_class_customizable_slots():
    class Slots(SlotsFields.a.b[1]):
        __slots__ = ["a", "b", "foo", "bar"]

    i = Slots(0)
    i.a = 1
    assert Slots.__slots__ == ["a", "b", "foo", "bar"]
    assert i.a == 1
    assert not hasattr(i, "__dict__")
    i.foo = 2
    assert i.foo == 2
    i.bar = 3
    assert i.bar == 3
    raises(AttributeError, setattr, i, "bogus", 1)
    raises(AttributeError, getattr, i, "bogus")


def test_defaults_on_tuples(impl):
    class Ok(impl.a.b['def']):
        pass
    assert Ok(1).b == 'def'
    assert Ok(1, 2).b == 2


def test_required_after_defaults(impl):
    def test():
        class Fail(impl.a['def'].b):
            pass

    raises(TypeError, test)


def test_extra_args(impl):
    raises(TypeError, impl.a.b, 1, 2, 3)


def test_comparable():
    class C(ComparableMixin.a):
        pass

    raises(TypeError, C, 1, 2, 3)

    class D(BareFields.a.b.c, ComparableMixin.a):
        pass

    assert D(1, 2, 3) == D(1, 3, 4)
    assert D(1, 2, 3) != D(2, 2, 3)


def test_printable():
    class D(BareFields.a.b.c, PrintableMixin.a.b):
        pass

    assert str(D(1, 2, 3)) == "D(a=1, b=2)"


def test_extra_args_2(impl):
    class X1(impl.a.b):
        pass

    raises(TypeError, X1, 1, 2, 3)


def test_missing_args(impl):
    raises(TypeError, impl.a.b, 1)


def test_missing_args_2(impl):
    class X1(impl.a.b):
        pass

    raises(TypeError, X1, 1)


def test_already_specified(impl):
    raises(TypeError, lambda: impl.a[1].a)


def test_already_specified_2(impl):
    raises(TypeError, lambda: impl.a.a)


def test_already_specified_3(impl):
    raises(TypeError, lambda: impl.a.a[2])


def test_already_specified_4(impl):
    raises(TypeError, lambda: impl.a.b.a)


def test_no_field(impl):
    raises(TypeError, lambda: impl[123])


def test_tuple_pickle(pickler, unpickler):
    g = G1(1, 2)
    assert unpickler(pickler(g)) == g


def test_class_pickle(pickler, unpickler):
    g = G2(1, c=0)
    assert unpickler(pickler(g)) == g


def test_slots_class_pickle(pickler, unpickler):
    g = G3(1, c=0)
    assert unpickler(pickler(g)) == g


def test_tuple_factory():
    class Z1(Tuple.a.b):
        pass

    t = Z1(1, 2)
    assert repr(t) == "Z1(a=1, b=2)"


def test_nosubclass(impl):
    T1 = impl.a.b.c[1].d[2]

    t = T1(1, 2)
    assert repr(t) == "FieldsBase(a=1, b=2, c=1, d=2)"


def test_factory(impl):
    class T1(impl.a.b.c[1].d[2]):
        pass

    t = T1(1, 2)
    assert repr(t) == "T1(a=1, b=2, c=1, d=2)"


def test_factory_all_defaults(impl):
    class T2(impl.a[0].b[1].c[2].d[3]):
        pass

    t = T2()
    assert repr(t) == "T2(a=0, b=1, c=2, d=3)"


def test_factory_no_required_after_defaults(impl):
    raises(TypeError, getattr, impl.a[0].b, 'c')


def test_factory_no_required_after_defaults_2(impl):
    raises(TypeError, type, 'Broken', (impl.a[0].b,), {})


def test_factory_t3(impl):
    class T3(impl.a):
        pass

    t = T3(1)
    assert repr(t) == "T3(a=1)"


def test_factory_empty_raise(impl):
    raises(TypeError, type, "T5", (impl,), {})


@fixture
def CmpC(request, impl):
    class CmpC(impl.a.b):
        pass

    return CmpC


def test_equal(CmpC):
    """
    Equal objects are detected as equal.
    """
    assert CmpC(1, 2) == CmpC(1, 2)
    assert not (CmpC(1, 2) != CmpC(1, 2))


def test_unequal_same_class(CmpC):
    """
    Unequal objects of correct type are detected as unequal.
    """
    assert CmpC(1, 2) != CmpC(2, 1)
    assert not (CmpC(1, 2) == CmpC(2, 1))


def test_unequal_different_class(CmpC):
    """
    Unequal objects of differnt type are detected even if their attributes
    match.
    """
    class NotCmpC(object):
        a = 1
        b = 2
    assert CmpC(1, 2) != NotCmpC()
    assert not (CmpC(1, 2) == NotCmpC())


def test_lt(CmpC):
    """
    __lt__ compares objects as tuples of attribute values.
    """
    for a, b in [
        ((1, 2),  (2, 1)),
        ((1, 2),  (1, 3)),
        (("a", "b"), ("b", "a")),
    ]:
        assert CmpC(*a) < CmpC(*b)


def test_lt_unordable(CmpC):
    """
    __lt__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (CmpC(1, 2).__lt__(42))


def test_le(CmpC):
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


def test_le_unordable(CmpC):
    """
    __le__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (CmpC(1, 2).__le__(42))


def test_gt(CmpC):
    """
    __gt__ compares objects as tuples of attribute values.
    """
    for a, b in [
        ((2, 1), (1, 2)),
        ((1, 3), (1, 2)),
        (("b", "a"), ("a", "b")),
    ]:
        assert CmpC(*a) > CmpC(*b)


def test_gt_unordable(CmpC):
    """
    __gt__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (CmpC(1, 2).__gt__(42))


def test_ne_unordable(CmpC):
    """
    __gt__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (CmpC(1, 2).__ne__(42))


def test_ge(CmpC):
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


def test_ge_unordable(CmpC):
    """
    __ge__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (CmpC(1, 2).__ge__(42))


def test_hash(CmpC):
    """
    __hash__ returns different hashes for different values.
    """
    assert hash(CmpC(1, 2)) != hash(CmpC(1, 1))


@fixture
def InitC(request, impl):
    class InitC(impl.a.b):
        def __init__(self, *args, **kwargs):
            super(InitC, self).__init__(*args, **kwargs)
            if self.a == self.b:
                raise ValueError

    return InitC


def test_sets_attributes(InitC):
    """
    The attributes are initialized using the passed keywords.
    """
    obj = InitC(a=1, b=2)
    assert 1 == obj.a
    assert 2 == obj.b


def test_custom_init(InitC):
    """
    The class initializer is called too.
    """
    with raises(ValueError):
        InitC(a=1, b=1)


def test_passes_args(InitC):
    """
    All positional parameters are passed to the original initializer.
    """
    class InitWithArg(Fields.a):
        def __init__(self, arg, **kwargs):
            super(InitWithArg, self).__init__(**kwargs)
            self.arg = arg

    obj = InitWithArg(42, a=1)
    assert 42 == obj.arg
    assert 1 == obj.a


def test_missing_arg(InitC):
    """
    Raises `ValueError` if a value isn't passed.
    """
    with raises(TypeError):
        InitC(a=1)


def test_regex_validator():
    class Test(RegexValidate.value['aa+'], Fields.value):
        pass

    raises(ValidationError, Test, 'a')
    raises(ValidationError, Test, '')
    raises(ValidationError, Test, 'bb')

    t = Test('aa')
    assert t.value == 'aa'


def test_regex_validator_rev():
    class Test(Fields.value, RegexValidate.value['aa+']):
        pass

    raises(ValidationError, Test, 'a')
    raises(ValidationError, Test, '')
    raises(ValidationError, Test, 'bb')

    t = Test('aa')
    assert t.value == 'aa'


def test_regex_validator_incompatible_layout():
    def test():
        class Test(RegexValidate.value['aa+'].extra['x'], Fields.value.extar['2'].a[3].b[4].c[5].d[6]):
            pass
    raises(TypeError, test)


def test_regex_validator_incompatible_layout_2():
    def test():
        class Test(RegexValidate.value['aa+'], Fields.other):
            pass
    raises(TypeError, test)


def test_regex_validator_bad_declaration():
    def test():
        class Test(RegexValidate.a.b['aa+']):
            pass
    raises(TypeError, test)


def test_regex_validator_fail_validation():
    class Test(RegexValidate.a['aa+']):
        pass
    raises(ValidationError, Test, 'a')


def test_regex_validator_rev_incompatible_layout(impl):
    def test():
        class Test(impl.value, RegexValidate.balue['aa+']):
            pass
    raises(TypeError, test)


def test_init_default_args_as_positional_args(impl):
    class MyContainer(impl.a.b[2].c[3]):
        pass

    assert repr(MyContainer(0, 1, 2)) == 'MyContainer(a=0, b=1, c=2)'


def test_init_default_args_as_positional_misaligned(impl):
    class MyContainer(impl.a.b[2].c[3]):
        pass

    raises(TypeError, MyContainer, 0, 1, b=2)


def test_init_default_args_as_positional_partial(impl):
    class MyContainer(impl.a.b[2].c[3]):
        pass

    assert repr(MyContainer(0, 1, c=2)) == 'MyContainer(a=0, b=1, c=2)'


def test_init_unknown_kwargs(impl):
    class MyContainer(impl.a.b[2].c[3]):
        pass

    raises(TypeError, MyContainer, 0, 1, x=2)


def test_init_too_many_positional(impl):
    class MyContainer(impl.a.b[2].c[3]):
        pass
    raises(TypeError, MyContainer, 0, 1, 2, 3)


def test_convertible():
    class TestContainer(ConvertibleFields.a.b):
        pass

    assert TestContainer(1, 2).as_dict == dict(a=1, b=2)


def test_convertible_mixin():
    class TestContainer(BareFields.a.b.c, ConvertibleMixin.a.b):
        pass

    assert TestContainer(1, 2, 3).as_tuple == (1, 2)
