characteristic
==============

.. image:: https://travis-ci.org/hynek/characteristic.svg
   :target: https://travis-ci.org/hynek/characteristic

.. image:: https://coveralls.io/repos/hynek/characteristic/badge.png?branch=master
    :target: https://coveralls.io/r/hynek/characteristic?branch=master

``characteristic`` is an MIT_-licensed package that eases the chores of implementing certain attribute-related object protocols in Python.
It’s inspired by Twisted’s `FancyEqMixin`_ but is implemented using class decorators because `sub-classing is bad for you`_, m’kay\ [*]_?

It’s tested on Python 2.6, 2.7, 3.3, 3.4, and PyPy.

.. [*] Just look at FancyEqMixin_\’s list of known subclasses and weep.


Examples
--------


Full Features
^^^^^^^^^^^^^

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


The difference to namedtuple_\ s is that classes decorated by ``characteristic`` are type-sensitive and just general classes you can use for whatever you want::


   >>> from __future__ import print_function
   >>> @attributes(["a",])
   ... class C1(object):
   ...     def print_a(self):
   ...         print(self.a)
   >>> @attributes(["a",])
   ... class C2(object):
   ...     pass
   >>> c1 = C1(a=1)
   >>> c2 = C2(a=1)
   >>> c1 == c2
   False
   >>> c1.print_a()
   1


…while namedtuple’s purpose is explicitly to behave like tuples::


   >>> from collections import namedtuple
   >>> NT1 = namedtuple("NT1", "a")
   >>> NT2 = namedtuple("NT2", "b")
   >>> t1 = NT1._make([1,])
   >>> t2 = NT2._make([1,])
   >>> t1 == t2
   True


Cherry Picking
^^^^^^^^^^^^^^

Of course, you can also use only *some* of the features by using ``with_cmp``, ``with_repr``, or ``with_init`` separately (or in any combination).


.. _FancyEqMixin: http://twistedmatrix.com/documents/current/api/twisted.python.util.FancyEqMixin.html
.. _`sub-classing is bad for you`: https://www.youtube.com/watch?v=3MNVP9-hglc
.. _MIT: http://choosealicense.com/licenses/mit/
.. _namedtuple: https://docs.python.org/2/library/collections.html#collections.namedtuple
.. _tuple: https://docs.python.org/2/tutorial/datastructures.html#tuples-and-sequences
