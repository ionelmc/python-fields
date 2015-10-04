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
import sys
from itertools import chain
from operator import itemgetter
try:
    from collections import OrderedDict
except ImportError:
    from .py2ordereddict import OrderedDict

__version__ = "3.0.0"

PY3 = sys.version_info[0] == 3
MISSING = object()


def _with_metaclass(meta, *bases):
    # See: http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/#metaclass-syntax-changes

    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})


class __base__(object):
    def __init__(self, *args, **kwargs):
        pass


def _make_init_func(required, defaults, everything,
                    header='def __init__(self',
                    call_start='super(FieldsBase, self).__init__(',
                    call_end=')\n',
                    kw=True, attrs=True):
    parts = [header]
    for var in everything:
        if var in defaults:
            parts.append(', {0}={0}'.format(var))
        else:
            parts.append(', {0}'.format(var))
    parts.append('):\n')
    if attrs:
        for var in everything:
            parts.append('    self.{0} = {0}\n'.format(var))
    parts.append('    ')
    parts.append(call_start)
    if kw:
        parts.append(', '.join('{0}={0}'.format(var) for var in everything))
    else:
        parts.append(', '.join('{0}'.format(var) for var in everything))
    parts.append(call_end)
    local_namespace = dict(defaults)
    global_namespace = dict(super=super)
    code = ''.join(parts)

    if PY3:
        exec(code, global_namespace, local_namespace)
    else:
        exec("exec code in global_namespace, local_namespace")
    return global_namespace, local_namespace


def class_sealer(required, defaults, everything,
                 base=__base__, make_init_func=_make_init_func,
                 initializer=True, comparable=True, printable=True, convertible=False):
    """
    This sealer makes a normal container class. It's mutable and supports arguments with default values.
    """
    if initializer:
        global_namespace, local_namespace = make_init_func(required, defaults, everything)

    class FieldsBase(base):
        if initializer:
            __init__ = local_namespace['__init__']

        if comparable:
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

        if printable:
            def __repr__(self):
                return "{0}({1})".format(
                    self.__class__.__name__,
                    ", ".join("{0}={1}".format(attr, repr(getattr(self, attr))) for attr in everything)
                )
        if convertible:
            @property
            def as_dict(self):
                return dict((attr, getattr(self, attr)) for attr in everything)

            @property
            def as_tuple(self):
                return tuple(getattr(self, attr) for attr in everything)

    if initializer:
        global_namespace['FieldsBase'] = FieldsBase
    return FieldsBase


def slots_class_sealer(required, defaults, everything):
    """
    This sealer makes a container class that uses ``__slots__`` (it uses :func:`class_sealer` internally).

    The resulting class has a metaclass that forcibly sets ``__slots__`` on subclasses.
    """
    class __slots_meta__(type):
        def __new__(mcs, name, bases, namespace):
            if "__slots__" not in namespace:
                namespace["__slots__"] = everything
            return type.__new__(mcs, name, bases, namespace)

    class __slots_base__(_with_metaclass(__slots_meta__, object)):
        __slots__ = ()

        def __init__(self, *args, **kwargs):
            pass

    return class_sealer(required, defaults, everything, base=__slots_base__)


def tuple_sealer(required, defaults, everything):
    """
    This sealer returns an equivalent of a ``namedtuple``.
    """
    global_namespace, local_namespace = _make_init_func(
        required, defaults, everything,
        header='def __new__(cls',
        call_start='return tuple.__new__(cls, (',
        call_end='))\n',
        kw=False, attrs=False,
    )

    def __getnewargs__(self):
        return tuple(self)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(a + "=" + repr(getattr(self, a)) for a in everything)
        )

    return type("TupleBase", (tuple,), dict(
        [(name, property(itemgetter(i))) for i, name in enumerate(everything)],
        __new__=local_namespace['__new__'],
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
    def __init__(self, func, **kwargs):
        self.func = func
        self.kwargs = kwargs

    @property
    def __name__(self):
        return self.func.__name__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **dict(self.kwargs, **kwargs))


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
        if name.startswith("__") and name.endswith("__"):
            return type.__getattribute__(cls, name)
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

    def __new__(mcs, name="__blank__", bases=(), namespace=None, last_field=None, required=(), defaults=(),
                sealer=Callable(class_sealer)):

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
            ), {} if namespace is None else namespace)

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


class Namespace(object):
    """
    A backport of Python 3.3's ``types.SimpleNamespace``.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ("{0}={1!r}".format(k, self.__dict__[k]) for k in keys)
        return "{0}({1})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


Fields = Factory()
ConvertibleFields = Factory(sealer=Callable(class_sealer, convertible=True))
SlotsFields = Factory(sealer=Callable(slots_class_sealer))
BareFields = Factory(sealer=Callable(class_sealer, comparable=False, printable=False))

Tuple = Factory(sealer=Callable(tuple_sealer))

PrintableMixin = Factory(sealer=Callable(class_sealer, initializer=False, base=object, comparable=False))
ComparableMixin = Factory(sealer=Callable(class_sealer, initializer=False, base=object, printable=False))
ConvertibleMixin = Factory(sealer=Callable(
    class_sealer, initializer=False, base=object, printable=False, comparable=False, convertible=True
))
