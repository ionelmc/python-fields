from itertools import chain
from operator import itemgetter
try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest

__version__ = "0.1.0"

MISSING = object()


def class_factory(required, defaults, everything):
    class FieldsBase(object):
        def __init__(self, *args, **kwargs):
            required_ = required

            for name, value in dict(defaults, **kwargs).items():
                if name in required:
                    required_ = tuple(n for n in required_ if n != name)

                setattr(self, name, value)
            for pos, (name, value) in enumerate(izip_longest(required_, args, fillvalue=MISSING)):
                if value is MISSING:
                    raise TypeError("Required argument %r (pos %s) not found" % (name, pos))
                elif name is MISSING:
                    raise TypeError("%s takes at most %s arguments (%s given)" % (
                        type(self).__name__, len(required_), len(args)
                    ))
                else:
                    setattr(self, name, value)

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in everything) == tuple(getattr(other, a) for a in everything)
            else:
                return NotImplemented

        def __ne__(self, other):
            result = self == other
            if result is NotImplemented:
                return NotImplemented
            else:
                return not result

        def __lt__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in everything) < tuple(getattr(other, a) for a in everything)
            else:
                return NotImplemented

        def __le__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in everything) <= tuple(getattr(other, a) for a in everything)
            else:
                return NotImplemented

        def __gt__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in everything) > tuple(getattr(other, a) for a in everything)
            else:
                return NotImplemented

        def __ge__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in everything) >= tuple(getattr(other, a) for a in everything)
            else:
                return NotImplemented

        def __hash__(self):
            return hash(tuple(getattr(self, a) for a in everything))

        def __repr__(self):
            return "<{0}({1})>".format(
                self.__class__.__name__,
                ", ".join(a + "=" + repr(getattr(self, a)) for a in everything)
            )
    return FieldsBase


def tuple_factory(required, defaults, everything):
    if defaults:
        raise TypeError("tuple_factory doesn't support default arguments")

    return type("TupleBase", (tuple,), dict(
        [(name, property(itemgetter(i))) for i, name in enumerate(required)],
        __new__=lambda cls, *args: tuple.__new__(cls, args),
        __dict__=property(lambda self: dict(zip(required, self))),
        __getnewargs__=lambda self: tuple(self),
        __repr__=lambda self: "<{0}({1})>".format(
            self.__class__.__name__,
            ", ".join(a + "=" + repr(getattr(self, a)) for a in everything)
        ),
    ))


def factory(field=None, required=(), defaults=(), sealer=class_factory):
    klass = None
    full_required = required
    if field is not None:
        full_required += field,
    all_fields = sorted(chain(full_required, defaults))

    class Meta(type):
        """
        This class makes everything work. It a metaclass for the class that this factory returns. Each new chain
        rebuilds everything.

        Workflow::

            class T(factory().a.b.c) breaks down to:
                m1 = class Meta
                c1 = instance of Meta
                    m1.__new__ => c1 (factory branch, c1 is not in bases)
                factory() => c1

                c1.__getattr__ resolves to m1.__getattr__, c1 is instance of m1
                c1.__getattr__('a') => factory('a')
                    m2 = class Meta
                    c2 = instance of Meta
                        m2.__new__ => c2 (factory branch, c2 is not in bases)

                c2.__getattr__ resolves to m2.__getattr__, c2 is instance of m2
                c2.__getattr__('b') => factory('b', ('a',))
                    m3 = class Meta
                    c3 = instance of Meta
                        m3.__new__ => c3 (factory branch, c3 is not in bases)

                c3.__getattr__ resolves to m3.__getattr__, c3 is instance of m3
                c3.__getattr__('c') => factory('c', ('a', 'b'))
                    m4 = class Meta
                    c4 = instance of Meta
                        m4.__new__ => c4 (factory branch, c4 is not in bases)

                class T(c4) => type("T", (c4,), {})
                    m4.__new__ => T (sealing branch, c4 is found bases)
                        returns type("T", (FieldsBase,), {}) instead
        """
        def __new__(mcs, name, bases, namespace):
            if klass in bases:
                if not all_fields:
                    raise TypeError("You're trying to use an empty Fields factory !")
                if defaults and field is not None:
                    raise TypeError("Can't add required fields after fields with defaults.")
                return type(name, tuple(
                    sealer(full_required, defaults, all_fields)
                    if k is klass else k for k in bases
                ), namespace)
            else:
                return type.__new__(mcs, name, bases, namespace)

        def __getattr__(cls, name):
            if name in required:
                raise ValueError("Field %r is already specified as required." % name)
            if name in defaults:
                raise ValueError("Field %r is already specified with a default value (%r)." % (
                    name, defaults[name]
                ))
            if defaults and field is not None:
                raise TypeError("Can't add required fields after fields with defaults.")
            return factory(name, full_required, defaults, sealer)

        def __call__(cls, default):
            if field is None:
                raise ValueError("Can't set default %r. There's no previous field." % default)

            new_defaults = {field: default}
            new_defaults.update(defaults)
            return factory(None, required, new_defaults, sealer)

    klass = Meta("Fields", (object,), {})
    return klass

Fields = factory()
Tuple = factory(sealer=tuple_factory)
