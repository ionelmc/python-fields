===============================
python-fields
===============================

.. image:: http://img.shields.io/travis/ionelmc/python-fields/master.png
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-fields

.. image:: https://ci.appveyor.com/api/projects/status/hrpb3ksl0sf1qyi8/branch/master
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-fields

.. image:: http://img.shields.io/coveralls/ionelmc/python-fields/master.png
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-fields

.. image:: http://img.shields.io/pypi/v/fields.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/fields

.. image:: http://img.shields.io/pypi/dm/fields.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/fields

Container class boilerplate killer.

Features:

* Human-readable ``__repr__``
* Complete set of comparison methods
* Keyword and positional argument support. Works like a normal class - you can override just about anything in the
  subclass (eg: a custom ``__init__``). In contrast, `hynek/characteristic <https://github.com/hynek/characteristic>`_
  forces different call schematics and calls your ``__init__`` with different arguments.


Installation
============

::

    pip install fields

Usage
=====

Make a class that has 2 attributes, ``a`` and ``b``::

    >>> from fields import Fields
    >>> class Pair(Fields.a.b):
    ...     pass
    ...
    >>> p = Pair(1, 2)
    >>> p.a
    1
    >>> p.b
    2

Make a class that has one required attribute ``value`` and two attributes (``left`` and ``right``) with default value
``None``::

    >>> class Node(Fields.value.left[None].right[None]):
    ...     pass
    ...
    >>> p = Node(1, left=Node(2), right=Node(3, left=Node(4)))
    >>> p
    Node(left=Node(left=None, right=None, value=2), right=Node(left=Node(left=None, right=None, value=4), right=None, value=3), value=1)

Want tuples?
-------------

Namedtuple alternative::

    >>> from fields import Tuple
    >>> class Pair(Tuple.a.b):
    ...     pass
    ...
    >>> p = Pair(1, 2)
    >>> p.a
    1
    >>> p.b
    2
    >>> tuple(p)
    (1, 2)
    >>> a, b = p
    >>> a
    1
    >>> b
    2

FAQ
===

Why should I use this?
-----------------------

It's less to type, why have quotes around when the names need to be valid symbols anyway. In fact, this is one
of the shortest forms possible to specify a container with fields.

But you're abusing a very well known syntax. You're using attribute access instead of a list of strings. Why?
--------------------------------------------------------------------------------------------------------------

Symbols should be symbols. Why validate strings so they are valid symbols when you can avoid that? Just use
symbols. Save on both typing and validation code.

The use of language constructs is not that surprising or confusing in the sense that semantics precede
conventional syntax use. For example, if we have ``class Person(Fields.first_name.last_name.height.weight): pass``
then it's going to be clear we're talking about a *Person* object with *first_name*, *last_name*, *height* and
*width* fields: the words have clear meaning.

Again, you should not name your varibles as `f1`, `f2` or any other non-semantic symbols anyway.

Semantics precede syntax: it's like looking at a cake resembling a dog, you won't expect the cake to bark and
run around.

Is this stable? Is it tested?
-------------------------------

Yes. Mercilessly tested on `Travis <https://travis-ci.org/ionelmc/python-fields>`_ and `AppVeyor
<https://ci.appveyor.com/project/ionelmc/python-fields>`_.

Is the API stable?
-------------------

Yes, ofcourse.

Why not ``namedtuple``?
------------------------

It's ugly, repetivive and unflexible. Compare this::

    >>> from collections import namedtuple
    >>> class MyContainer(namedtuple("MyContainer", ["field1", "field2"])):
    ...     pass
    >>> MyContainer(1, 2)
    MyContainer(field1=1, field2=2)

To this::

    >>> class MyContainer(Tuple.field1.field2):
    ...     pass
    >>> MyContainer(1, 2)
    MyContainer(field1=1, field2=2)

Why not ``characteristic``?
----------------------------

Ugly, inconsistent - you don't own the class:

    Lets try this::

        >>> import characteristic
        >>> @characteristic.attributes(["field1", "field2"])
        ... class MyContainer(object):
        ...     def __init__(self, a, b):
        ...         if a > b:
        ...             raise ValueError("Expected %s < %s" % (a, b))
        >>> MyContainer(1, 2)
        Traceback (most recent call last):
            ...
        ValueError: Missing keyword value for 'field1'.

    WHAT !? Ok, lets write some more code::

        >>> MyContainer(field1=1, field2=2)
        Traceback (most recent call last):
            ...
        TypeError: __init__() ... arguments...

    This is bananas. You have to write your class *around* these quirks.

Lets try this::

    >>> class MyContainer(Fields.field1.field2):
    ...     def __init__(self, a, b):
    ...         if a > b:
    ...             raise ValueError("Expected %s < %s" % (a, b))
    ...         super(MyContainer, self).__init__(a, b)

Just like a normal class, works as expected::

    >>> MyContainer(1, 2)
    MyContainer(field1=1, field2=2)


Documentation
=============

https://python-fields.readthedocs.org/

Development
===========

To run the all tests run::

    tox
