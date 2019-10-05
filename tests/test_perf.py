from collections import namedtuple
from functools import partial

import pytest
from attr import Factory
from attr import ib as badly_named_field
from attr import make_class
from attr import s as badly_named_class_decorator
from characteristic import Attribute
from characteristic import attributes

from fields import Fields
from fields import SlotsFields
from fields import Tuple
from fields import __base__
from fields import class_sealer
from fields import factory
from fields import make_init_func

try:
    from cnamedtuple import namedtuple as cnamedtuple
except ImportError:
    cnamedtuple = None


@attributes(["a", "b", Attribute("c", default_value="abc")])
class characteristic_class(object):
    pass


@badly_named_class_decorator
class attrs_decorated_class(object):
    a = badly_named_field()
    b = badly_named_field()
    c = badly_named_field(default=Factory("abc"))


class fields_nosuper_class(
    factory(
        class_sealer,
        base=object,
        make_init_func=partial(make_init_func, super_call=False)
    ).a.b.c["abc"]
):
    pass


class fields_class(Fields.a.b.c["abc"]):
    pass


class slots_class(SlotsFields.a.b.c["abc"]):
    pass


class tuple_class(Tuple.a.b.c["abc"]):
    pass


def make_super_dumb_class():
    class super_dumb_class(__base__):
        def __init__(self, a, b, c="abc"):
            self.a = a
            self.b = b
            self.c = c
            super(super_dumb_class, self).__init__(a=a, b=b, c=c)

    return super_dumb_class


super_dumb_class = make_super_dumb_class()


class dumb_class(object):
    def __init__(self, a, b, c="abc"):
        self.a = a
        self.b = b
        self.c = c


namedtuple_class = namedtuple("namedtuple_class", ["a", "b", "c"])
if cnamedtuple:
    cnamedtuple_class = cnamedtuple("namedtuple_class", ["a", "b", "c"])
else:
    def cnamedtuple_class(*args, **kwargs):
        pytest.skip("Not available.")
attrs_class = make_class("attrs_class", ["a", "b", "c"])


def test_characteristic(benchmark):
    assert benchmark(partial(characteristic_class, a=1, b=2, c=1))


def test_fields(benchmark):
    assert benchmark(partial(fields_class, a=1, b=2, c=1))


def test_fields_nosuper(benchmark):
    assert benchmark(partial(fields_nosuper_class, a=1, b=2, c=1))


def test_slots_fields(benchmark):
    assert benchmark(partial(slots_class, a=1, b=2, c=1))


def test_super_dumb(benchmark):
    assert benchmark(partial(super_dumb_class, a=1, b=2, c=1))


def test_dumb(benchmark):
    assert benchmark(partial(dumb_class, a=1, b=2, c=1))


def test_tuple(benchmark):
    assert benchmark(partial(tuple_class, a=1, b=2, c=1))


def test_namedtuple(benchmark):
    assert benchmark(partial(namedtuple_class, a=1, b=2, c=1))


def test_cnamedtuple(benchmark):
    assert benchmark(partial(cnamedtuple_class, a=1, b=2, c=1))


def test_attrs_decorated_class(benchmark):
    assert benchmark(partial(attrs_decorated_class, a=1, b=2, c=1))


def test_attrs_class(benchmark):
    assert benchmark(partial(attrs_class, a=1, b=2, c=1))
