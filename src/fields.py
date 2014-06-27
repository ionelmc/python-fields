from itertools import chain
from itertools import izip_longest

__version__ = "0.1.0"

MISSING = object()


def factory(field=None, required=(), defaults=(), ancestor=None):
    klass = None
    full_required = required
    if field is not None:
        full_required += field,
    all_fields = sorted(chain(full_required, defaults))

    class FieldsBase(object):
        def __init__(self, *args, **kwargs):
            required_ = full_required

            for name, value in dict(defaults, **kwargs).items():
                if name in full_required:
                    required_ = tuple(n for n in required if n != name)
                else:
                    setattr(self, name, value)
            for pos, (name, value) in enumerate(izip_longest(required_, args, fillvalue=MISSING)):
                if value is MISSING:
                    raise TypeError("Required argument %r (pos %s) not found" % (name, pos))
                elif name is MISSING:
                    raise TypeError("%s takes at most %s arguments (%s given)" % (
                        type(self).__name__, len(required), len(args)
                    ))
                else:
                    setattr(self, name, value)

        def __repr__(self):
            return "<{0}({1})>".format(
                self.__class__.__name__,
                ", ".join(a + "=" + repr(getattr(self, a)) for a in all_fields)
            )

    class Meta(type):
        def __new__(mcs, name, bases, namespace):
            #print '__new__', mcs, name, bases, namespace
            #print '       ', ancestor in bases, klass in bases, klass is mcs, klass is ancestor, mcs is ancestor
            #if bases:
            #    print '    ***', bases[0] is klass
            if klass in bases:
                return type(name, tuple(FieldsBase if k is klass else k for k in bases), namespace)
            else:
                return type.__new__(mcs, name, bases, namespace)

        def __getattr__(cls, name):
            if name in required:
                raise ValueError("Field %r is already specified as required." % name)
            if name in defaults:
                raise ValueError("Field %r is already specified with a default value (%r)." % (
                    name, defaults[name]
                ))
            return factory(name, required if field is None else required + (field,), defaults, Meta)

        def __call__(cls, default):
            if field is None:
                raise ValueError("Can't set default %r. There's no previous field." % default)

            defaults = {field: default}
            defaults.update(defaults)
            return factory(None, required, defaults, Meta)

    klass = Meta("Fields", (object,), {})
    return klass

Fields = factory()

def with_cmp(attrs):
    """
    A class decorator that adds comparison methods based on *attrs*.

    Two instances are compared as if the respective values of *attrs* were
    tuples.

    :param attrs: Attributes to work with.
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
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) < attrs_to_tuple(other)
        else:
            return NotImplemented

    def le(self, other):
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) <= attrs_to_tuple(other)
        else:
            return NotImplemented

    def gt(self, other):
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) > attrs_to_tuple(other)
        else:
            return NotImplemented

    def ge(self, other):
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) >= attrs_to_tuple(other)
        else:
            return NotImplemented

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

