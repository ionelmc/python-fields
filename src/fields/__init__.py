"""
How it works: the library is composed of 2 major parts:

* The `sealers`. They return a class that implements a container according the given specification (list of field names
  and default values).
* The `Factory`. A metaclass that implements attribute/item access, so you can do ``Fields.a.b.c``. On each
  getattr/getitem it returns a new instance with the new state. Its ``__new__`` method takes extra arguments to store
  the contruction state and it works in two ways:

  * Construction phase (there are no bases). Make new instances of the `Factory` with new state.
  * Usage phase. When subclassed (there are bases) it will use the sealer to return the final class.
"""
import re
from itertools import chain
from operator import itemgetter
try:
    from collections import OrderedDict
except ImportError:
    from .py2ordereddict import OrderedDict

__version__ = "1.0.2"

MISSING = object()


class __base__(object):
    def __init__(self, *args, **kwargs):
        pass


def class_sealer(required, defaults, everything):
    """
    This sealer make a normal container class. It's mutable and supports arguments with default values.
    """
    class FieldsBase(__base__):
        def __init__(self, *args, **kwargs):
            arguments = OrderedDict(zip(everything, args))
            if len(args) > len(everything):
                raise TypeError("__init__() takes at most %s arguments (%s given)" % (len(everything), len(args)))
            for name, value in kwargs.items():
                if name in arguments:
                    raise TypeError("__init__() got multiple values for keyword argument %r" % name)
                elif name not in everything:
                    raise TypeError("__init__() got an unexpected keyword argument %r" % name)
                else:
                    arguments[name] = value
            for pos, name in enumerate(required):
                if name not in arguments:
                    raise TypeError("__init__() requires argument %r (at position %s)" % (name, pos))
            if defaults:
                for name, value in defaults.items():
                    if name not in arguments:
                        arguments[name] = value
            for name, value in arguments.items():
                setattr(self, name, value)

            super(FieldsBase, self).__init__(*args, **kwargs)

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return tuple(getattr(self, a) for a in everything) == tuple(getattr(other, a) for a in everything)
            else:
                return NotImplemented

        def __ne__(self, other):
            result = self.__eq__(other)
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
            return "{0}({1})".format(
                self.__class__.__name__,
                ", ".join(a + "=" + repr(getattr(self, a)) for a in everything)
            )
    return FieldsBase


def tuple_sealer(required, defaults, everything):
    """
    This sealer returns an equivalent of a ``namedtuple``.
    """
    if defaults:
        raise TypeError("tuple_sealer doesn't support default arguments")

    def __new__(cls, *args):
        return tuple.__new__(cls, args)

    def __getnewargs__(self):
        return tuple(self)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(a + "=" + repr(getattr(self, a)) for a in everything)
        )

    return type("TupleBase", (tuple,), dict(
        [(name, property(itemgetter(i))) for i, name in enumerate(required)],
        __new__=__new__,
        __getnewargs__=__getnewargs__,
        __repr__=__repr__,
        __slots__=(),
    ))


class Callable(object):
    """
    Primitive wrapper around a function that makes it `un-bindable`.

    When you add a function in the namespace of a class it will be bound (become a method) when you try to access it.
    This class prevents that.
    """
    def __init__(self, func):
        self.func = func

    @property
    def __name__(self):
        return self.func.__name__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Factory(type):
    """
    This class makes everything work. It a metaclass for the class that users are going to use. Each new chain
    rebuilds everything.
    """

    __required = ()
    __defaults = ()
    __all_fields = ()
    __last_field = None
    __full_required = ()
    __sealer = None
    __concrete = None

    def __getattr__(cls, name):
        if name in cls.__required:
            raise TypeError("Field %r is already specified as required." % name)
        if name in cls.__defaults:
            raise TypeError("Field %r is already specified with a default value (%r)." % (
                name, cls.__defaults[name]
            ))
        if name == cls.__last_field:
            raise TypeError("Field %r is already specified as required." % name)
        if cls.__defaults and cls.__last_field is not None:
            raise TypeError("Can't add required fields after fields with defaults.")

        return Factory(
            required=cls.__full_required,
            defaults=cls.__defaults,
            last_field=name,
            sealer=cls.__sealer,
        )

    def __getitem__(cls, default):
        if cls.__last_field is None:
            raise TypeError("Can't set default %r. There's no previous field." % default)

        new_defaults = OrderedDict(cls.__defaults)
        new_defaults[cls.__last_field] = default
        return Factory(
            required=cls.__required,
            defaults=new_defaults,
            sealer=cls.__sealer,
        )

    def __new__(mcs, name="__blank__", bases=(), namespace={}, last_field=None, required=(), defaults=(), sealer=Callable(class_sealer)):
        if not bases:
            assert isinstance(sealer, Callable)

            full_required = tuple(required)
            if last_field is not None:
                full_required += last_field,
            all_fields = list(chain(full_required, defaults))

            return type.__new__(
                Factory,
                "Fields<%s>.%s" % (sealer.__name__, ".".join(all_fields))
                if all_fields else "Fields<%s>" % sealer.__name__,
                bases,
                dict(
                    _Factory__required=required,
                    _Factory__defaults=defaults,
                    _Factory__all_fields=all_fields,
                    _Factory__last_field=last_field,
                    _Factory__full_required=full_required,
                    _Factory__sealer=sealer,
                )
            )
        else:
            for pos, names in enumerate(zip(*[
                k.__all_fields
                for k in bases
                if isinstance(k, Factory)
            ])):
                if names:
                    if len(set(names)) != 1:
                        raise TypeError("Field layout conflict: fields in position %s have different names: %s" % (
                            pos,
                            ', '.join(repr(name) for name in names)
                        ))

            return type(name, tuple(
                ~k if isinstance(k, Factory) else k for k in bases
            ), namespace)

    def __init__(cls, *args, **kwargs):
        pass

    def __call__(cls, *args, **kwargs):
        return (~cls)(*args, **kwargs)

    def __invert__(cls):
        if cls.__concrete is None:
            if not cls.__all_fields:
                raise TypeError("You're trying to use an empty Fields factory !")
            if cls.__defaults and cls.__last_field is not None:
                raise TypeError("Can't add required fields after fields with defaults.")

            cls.__concrete = cls.__sealer(cls.__full_required, cls.__defaults, cls.__all_fields)
        return cls.__concrete


class ValidationError(Exception):
    pass


def regex_validation_sealer(required, defaults, everything, RegexType=type(re.compile(""))):
    """
    Example sealer that just does regex-based validation.
    """
    if required:
        raise TypeError("regex_validation_sealer doesn't support required arguments")

    klass = None
    kwarg_validators = dict(
        (key, val if isinstance(val, RegexType) else re.compile(val)) for key, val in defaults.items()
    )
    arg_validators = list(
        kwarg_validators[key] for key in everything
    )

    def __init__(self, *args, **kwargs):
        for pos, (value, validator) in enumerate(zip(args, arg_validators)):
            if not validator.match(value):
                raise ValidationError("Positional argument %s failed validation. %r doesn't match regex %r" % (
                    pos, value, validator.pattern
                ))
        for key, value in kwargs.items():
            if key in kwarg_validators:
                validator = kwarg_validators[key]
                if not validator.match(value):
                    raise ValidationError("Keyword argument %r failed validation. %r doesn't match regex %r" % (
                        key, value, validator.pattern
                    ))
        super(klass, self).__init__(*args, **kwargs)

    klass = type("RegexValidateBase", (__base__,), dict(
        __init__=__init__,
    ))
    return klass

Fields = Factory()
Tuple = Factory(sealer=Callable(tuple_sealer))
RegexValidate = Factory(sealer=Callable(regex_validation_sealer))
