from itertools import chain
from itertools import izip_longest

__version__ = "0.1.0"

MISSING = object()


def factory(field=None, required=(), defaults=()):
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
                    required_ = tuple(n for n in required_ if n != name)

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

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in all_fields) == tuple(getattr(other, a) for a in all_fields)
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
                return tuple(getattr(self, a) for a in all_fields) < tuple(getattr(other, a) for a in all_fields)
            else:
                return NotImplemented

        def __le__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in all_fields) <= tuple(getattr(other, a) for a in all_fields)
            else:
                return NotImplemented

        def __gt__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in all_fields) > tuple(getattr(other, a) for a in all_fields)
            else:
                return NotImplemented

        def __ge__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in all_fields) >= tuple(getattr(other, a) for a in all_fields)
            else:
                return NotImplemented

        def __hash__(self):
            return hash(tuple(getattr(self, a) for a in all_fields))

        def __repr__(self):
            return "<{0}({1})>".format(
                self.__class__.__name__,
                ", ".join(a + "=" + repr(getattr(self, a)) for a in all_fields)
            )

    class Meta(type):
        def __new__(mcs, name, bases, namespace):
            if klass in bases:
                if not all_fields:
                    raise TypeError("You're trying to use an empty Fields factory !")
                if defaults and field is not None:
                    raise TypeError("Can't add required fields after fields with defaults.")
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
            if defaults and field is not None:
                raise TypeError("Can't add required fields after fields with defaults.")
            return factory(name, full_required, defaults)

        def __call__(cls, default):
            if field is None:
                raise ValueError("Can't set default %r. There's no previous field." % default)

            new_defaults = {field: default}
            new_defaults.update(defaults)
            return factory(None, required, new_defaults)

    klass = Meta("Fields", (object,), {})
    return klass

Fields = factory()


