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

Let’s start with all bells and whistles: ``with_attributes`` will add a nice ``__repr__``, comparison methods that compare instances as if their respective attributes would be tuple_\ s, and -- optionally -- an initializer to your class::

   >>> from characteristic import with_attributes
   >>> @with_attributes(("a", "b",), create_init=True)
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


The difference to namedtuple_\ s is that classes decorated by ``characteristic`` are type-sensitive and just general classes you can use for whatever you want::

   >>> from __future__ import print_function
   >>> @with_attributes(("a",), create_init=True)
   ... class C1(object):
   ...     def print_a(self):
   ...         print(self.a)
   >>> @with_attributes(("a",), create_init=True)
   ... class C2(object):
   ...     pass
   >>> c1 = C1(a=1)
   >>> c2 = C2(a=1)
   >>> c1 == c2
   False
   >>> c1.print_a()
   1


While namedtuple’s purpose is explicitly to behave like tuples::


   >>> from collections import namedtuple
   >>> NT1 = namedtuple("NT1", "a")
   >>> NT2 = namedtuple("NT2", "b")
   >>> t1 = NT1._make((1,))
   >>> t2 = NT2._make((1,))
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
