.. _examples:

Examples
========


Full Features
-------------

Let’s start with all bells and whistles: ``@attributes([attr1, attr2, …])`` enhances your class by:

- a nice ``__repr__``,
- comparison methods that compare instances as if they were tuples of their attributes,
- and – optionally but by default – an initializer that uses the keyword arguments to initialize the specified attributes before running the class’ own initializer.

::

   >>> from characteristic import attributes
   >>> @attributes(["a", "b",])
   ... class C(object):
   ...     pass
   >>> obj1 = C(a=1, b="abc")
   >>> obj1
   <C(a=1, b='abc')>
   >>> obj2 = C(a=2, b="abc")
   >>> obj1 == obj2
   False
   >>> obj1 < obj2
   True
   >>> obj3 = C(a=1, b="bca")
   >>> obj3 > obj1
   True
   >>> @attributes(["a", "b", "c",], defaults={"c": 3})
   ... class CWithDefaults(object):
   ...     pass
   >>> obj4 = CWithDefaults(a=1, b=2)
   >>> obj5 = CWithDefaults(a=1, b=2, c=3)
   >>> obj4 == obj5
   True




Cherry Picking
--------------

Of course, you can also use only *some* of the features by using ``with_cmp``, ``with_repr``, or ``with_init`` separately (or in any combination).
