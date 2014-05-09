from __future__ import absolute_import, division, print_function


__version__ = "0.1.0dev"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2014 Hynek Schlawack"


def with_cmp(attrs):
    """
    A class decorator that adds comparison methods based on *attrs*.

    Two instances are compared as if the respective  values of *attrs* were
    tuples.

    :param attrs: Attributes that are compared.
    :type attrs: `list` of native strings
    """
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

    def wrap(cl):
        cl.__eq__ = eq
        cl.__ne__ = ne
        cl.__lt__ = lt
        cl.__le__ = le
        cl.__gt__ = gt
        cl.__ge__ = ge
        cl.__hash__ = hash_

        return cl
    return wrap


def with_repr(attrs):
    """
    A class decorator that adds a __repr__ method that returns a sensible
    representation based on *attrs*.
    """
    def repr_(self):
        return "<{0}({1})>".format(
            self.__class__.__name__,
            ", ".join(a + "=" + repr(getattr(self, a)) for a in attrs)
        )

    def wrap(cl):
        cl.__repr__ = repr_
        return cl

    return wrap


def with_init(attrs):
    """
    A class decorator that wraps the __init__ method of a class and sets
    *attrs* first using keyword arguments.
    """
    def init(self, *args, **kw):
        for a in attrs:
            setattr(self, a, kw.pop(a))
        self.__original_init__(*args, **kw)

    def wrap(cl):
        cl.__original_init__ = cl.__init__
        cl.__init__ = init
        return cl

    return wrap


def attributes(attrs, create_init=True):
    """
    A class decorator that combines :func:`with_cmp` and :func:`with_repr` to
    avoid code duplication.

    Optionally also apply :func:`with_init`.
    """
    def wrap(cl):
        cl = with_cmp(attrs)(with_repr(attrs)(cl))
        if create_init is True:
            return with_init(attrs)(cl)
        else:
            return cl
    return wrap
