.. _api:

API
===

``characteristic`` consists of class decorators that add features to your classes..
There are three that start with ``@with_`` that add *one* feature to your class based on a list of attributes.
Then there's the helper ``@attributes`` that combines them all into one decorator so you don't have to repeat the attribute list multiple times.

.. currentmodule:: characteristic


.. decorator:: with_repr(attrs)

   A class decorator that adds a human readable ``__repr__`` method to your class using *attrs*.

   .. doctest::

      >>> from characteristic import with_repr
      >>> @with_repr(["a", "b"])
      ... class RClass(object):
      ...     def __init__(self, a, b):
      ...         self.a = a
      ...         self.b = b
      >>> c = RClass(42, "abc")
      >>> print c
      <RClass(a=42, b='abc')>


   :param attrs: Attributes to work with.
   :type attrs: `list` of native strings


.. decorator:: with_cmp(attrs)

   A class decorator that adds comparison methods based on *attrs*.

   For that, each class is treated like a `tuple` of the values of *attrs*.

   .. doctest::

      >>> from characteristic import with_cmp
      >>> @with_cmp(["a", "b"])
      ... class CClass(object):
      ...     def __init__(self, a, b):
      ...         self.a = a
      ...         self.b = b
      >>> o1 = CClass(1, "abc")
      >>> o2 = CClass(1, "abc")
      >>> o1 == o2  # o1.a == o2.a and o1.b == o2.b
      True
      >>> o1.c = 23
      >>> o2.c = 42
      >>> o1 == o2  # attributes that are not passed to with_cmp are ignored
      True
      >>> o3 = CClass(2, "abc")
      >>> o1 < o3  # because 1 < 2
      True
      >>> o4 = CClass(1, "bca")
      >>> o1 < o4  # o1.a == o4.a, but o1.b < o4.b
      True


   :param attrs: Attributes to work with.
   :type attrs: `list` of native strings


.. decorator:: with_init(attrs, defaults=None)

   A class decorator that wraps the ``__init__`` method of a class and sets
   *attrs* using passed keyword arguments before calling the original
   ``__init__``.

   Those keyword arguments that are used, are removed from the `kwargs` that is passed into your original ``__init__``.
   Optionally, a dictionary of default values for some of *attrs* can be passed too.

   .. doctest::

      >>> from characteristic import with_init
      >>> @with_init(["a", "b"], defaults={"b": 2})
      ... class IClass(object):
      ...     def __init__(self):
      ...         if self.b != 2:
      ...             raise ValueError("'b' must be 2!")
      >>> o1 = IClass(a=1, b=2)
      >>> o2 = IClass(a=1)
      >>> o1.a == o2.a
      True
      >>> o1.b == o2.b
      True
      >>> IClass()
      Traceback (most recent call last):
        ...
      ValueError: Missing value for 'a'.
      >>> IClass(a=1, b=3)  # the custom __init__ is called after the attributes are initialized
      Traceback (most recent call last):
        ...
      ValueError: 'b' must be 2!


   :param attrs: Attributes to work with.
   :type attrs: `list` of native strings

   :param defaults: Default values if attributes are omitted on instantiation.
   :type defaults: `dict` or `None`

   :raises ValueError: If the value for a non-optional attribute hasn't been passed.


.. decorator:: attributes(attrs, defaults=None, create_init=True)

   A convenience class decorator that combines :func:`with_cmp`,
   :func:`with_repr`, and optionally :func:`with_init` to avoid code
   duplication.


   See :doc:`examples` for ``@attributes`` in action!

   :param attrs: Attributes to work with.
   :type attrs: Iterable of native strings.

   :param defaults: Default values if attributes are omitted on instantiation.
   :type defaults: `dict` or `None`

   :param create_init: Also apply :func:`with_init` (default: `True`)
   :type create_init: `bool`

   :raises ValueError: If the value for a non-optional attribute hasn't been passed.
