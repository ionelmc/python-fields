from __future__ import absolute_import, division, print_function


__version__ = "0.1.0dev"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2014 Hynek Schlawack"


def eq_attrs(attrs):
    """
    Adds __eq__, and __ne__ methods based on *attrs* and same type.

    __lt__, __le__, __gt__, and __ge__ compare the objects as if it were tuples
    of attrs.

    :param attrs: Attributes that have to be equal to make two instances equal.
    :type attrs: `list` of native strings
    """
    def wrap(cl):
        def eq(self, other):
            if isinstance(other, self.__class__):
                return all(
                    getattr(self, a) == getattr(other, a)
                    for a in attrs
                )
            else:
                return False

        def ne(self, other):
            return not eq(self, other)

        def attrs_to_tuple(obj):
            return tuple(getattr(obj, a) for a in attrs)

        def lt(self, other):
            return attrs_to_tuple(self) < attrs_to_tuple(other)

        def le(self, other):
            return attrs_to_tuple(self) <= attrs_to_tuple(other)

        def gt(self, other):
            return attrs_to_tuple(self) > attrs_to_tuple(other)

        def ge(self, other):
            return attrs_to_tuple(self) >= attrs_to_tuple(other)

        cl.__eq__ = eq
        cl.__ne__ = ne
        cl.__lt__ = lt
        cl.__le__ = le
        cl.__gt__ = gt
        cl.__ge__ = ge

        return cl
    return wrap


def repr_attrs(attrs):
    """
    Adds a __repr__ method that returns a sensible representation based on
    *attrs*.
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
    Combine :func:`eq_attrs` and :func:`repr_attrs` to avoid code duplication.
    """
    def wrap(cl):
        return eq_attrs(attrs)(repr_attrs(attrs)(cl))
    return wrap
