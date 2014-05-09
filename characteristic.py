from __future__ import absolute_import, division, print_function


__version__ = "0.1.0dev"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2014 Hynek Schlawack"


def cmp_attrs(attrs):
    """
    A class decorator that adds comparison methods based on *attrs*.

    Two instances are compared as if the respective  values of *attrs* were
    tuples.

    :param attrs: Attributes that are compared.
    :type attrs: `list` of native strings
    """
    def wrap(cl):
        def attrs_to_tuple(obj):
            """
            Create a tuple of all values of *obj*'s *attrs*.
            """
            return tuple(getattr(obj, a) for a in attrs)

        def eq(self, other):
            if isinstance(other, self.__class__):
                return attrs_to_tuple(self) == attrs_to_tuple(other)
            else:
                return NotImplemented

        def ne(self, other):
            result = eq(self, other)
            if result is NotImplemented:
                return NotImplemented
            else:
                return not result

        def lt(self, other):
            return attrs_to_tuple(self) < attrs_to_tuple(other)

        def le(self, other):
            return attrs_to_tuple(self) <= attrs_to_tuple(other)

        def gt(self, other):
            return attrs_to_tuple(self) > attrs_to_tuple(other)

        def ge(self, other):
            return attrs_to_tuple(self) >= attrs_to_tuple(other)

        def hash_(self):
            return hash(attrs_to_tuple(self))

        cl.__eq__ = eq
        cl.__ne__ = ne
        cl.__lt__ = lt
        cl.__le__ = le
        cl.__gt__ = gt
        cl.__ge__ = ge
        cl.__hash__ = hash_

        return cl
    return wrap


def repr_attrs(attrs):
    """
    A class decorator that adds a __repr__ method that returns a sensible
    representation based on *attrs*.
    """
    def wrap(cl):
        def repr_(self):
            return "<{0}({1})>".format(
                self.__class__.__name__,
                ", ".join(a + "=" + repr(getattr(self, a)) for a in attrs)
            )

        cl.__repr__ = repr_
        return cl

    return wrap


def magic_attrs(attrs):
    """
    Combine :func:`cmp_attrs` and :func:`repr_attrs` to avoid code duplication.
    """
    def wrap(cl):
        return cmp_attrs(attrs)(repr_attrs(attrs)(cl))
    return wrap
