from pytest import mark
from collections import namedtuple

from characteristic import Attribute
from characteristic import attributes

from fields import __base__
from fields import Fields


@attributes(["a", "b", Attribute("c", default_value="abc")])
class characteristic_class(object):
    pass


class fields_class(Fields.a.b.c["abc"]):
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


def test_characteristic(benchmark):
    with benchmark:
        assert characteristic_class(a=1, b=2, c=1)


def test_fields(benchmark):
    with benchmark:
        assert fields_class(a=1, b=2, c=1)


def test_super_dumb(benchmark):
    with benchmark:
        assert super_dumb_class(a=1, b=2, c=1)


def test_dumb(benchmark):
    with benchmark:
        assert dumb_class(a=1, b=2, c=1)

def test_namedtuple(benchmark):
    with benchmark:
        assert namedtuple_class(a=1, b=2, c=1)
