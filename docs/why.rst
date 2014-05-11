.. _why:

Why?
====

The difference between namedtuple_\ s and classes decorated by ``characteristic`` is that the latter are type-sensitive and less typing aside regular classes:


.. doctest::

   >>> from characteristic import attributes
   >>> @attributes(["a",])
   ... class C1(object):
   ...     def print_a(self):
   ...         print self.a
   >>> @attributes(["a",])
   ... class C2(object):
   ...     pass
   >>> c1 = C1(a=1)
   >>> c2 = C2(a=1)
   >>> c1 == c2
   False
   >>> c1.print_a()
   1


…while namedtuple’s purpose is *explicitly* to behave like tuples:


.. doctest::

   >>> from collections import namedtuple
   >>> NT1 = namedtuple("NT1", "a")
   >>> NT2 = namedtuple("NT2", "b")
   >>> t1 = NT1._make([1,])
   >>> t2 = NT2._make([1,])
   >>> t1 == t2 == (1,)
   True


This can easily lead to surprising and unintended behaviors.

.. _namedtuple: https://docs.python.org/2/library/collections.html#collections.namedtuple
.. _tuple: https://docs.python.org/2/tutorial/datastructures.html#tuples-and-sequences
