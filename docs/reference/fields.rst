fields
=============================


.. automodule:: fields
    :members:

.. class:: fields.Fields

    Container class generator. The resulting class will implement ``__repr__``, ``__init__``, ``__eq__``, ``__ne__``, ``__lt__``,
    ``__gt__``, ``__le__``, ``__ge__`` and ``__hash__``.

    Usage:

    .. sourcecode:: python

        class Foobar(Fields.foo.bar):
            pass

.. class:: fields.BareFields

    Container class generator. The resulting class will implement ``__init__``.

    Usage:

    .. sourcecode:: python

        class Foobar(BareFields.foo.bar):
            pass

.. class:: fields.PrintableMixin

    Container class generator. The resulting class will implement ``__repr__``.

    Usage:

    .. sourcecode:: python

        class Foobar(PrintableMixin.foo.bar):
            # we need to have the `foo` and `bar` attributes
            foo = None
            bar = None

.. class:: fields.ComparableMixin

    Container class generator. The resulting class will implement ``__eq__``, ``__ne__``, ``__lt__``,
    ``__gt__``, ``__le__``, ``__ge__`` and ``__hash__``.

    Usage:

    .. sourcecode:: python


        class Foobar(BareFields.name.extra, ComparableMixin.name):
            """
            A class that only compares on `name` but has an `extra` field.
            """
            pass

