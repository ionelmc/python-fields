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
    <Node(left=<Node(left=None, right=None, value=2)>, right=<Node(left=<Node(left=None, right=None, value=4)>, right=None, value=3)>, value=1)>

Want tuples ?
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

:Q: Why ???
:A: It's less to type, why have quotes around when the names need to be valid symbols anyway.

..

:Q: Really ... why ???
:A: Because it's possible.

..

:Q: But you're abusing a very well known syntax. You're using attribute access instead of a list of strings. Why ?
:A: Yes. [*]_

..

:Q: What's good about this ?
:A: It's one of the shortest forms possible.

..

:Q: Is this stable ? Is it tested ?
:A:
    Yes. Mercilessly tested on `Travis <https://travis-ci.org/ionelmc/python-fields>`_ and `AppVeyor
    <https://ci.appveyor.com/project/ionelmc/python-fields>`_.

..

:Q: Is the API stable ?
:A: It can't get worse can it ;)

..

:Q: Why not ``namedtuple`` ?
:A:
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
        <MyContainer(field1=1, field2=2)>

..

:Q: Why not ``characteristic`` ?
:A:
    Ugly, inconsistent - you don't own the class:

        Lets try this:

            >>> import characteristic
            >>> @characteristic.attributes(["field1", "field2"])
            ... class MyContainer(object):
            ...     def __init__(self, a, b):
            ...         if a > b:
            ...             raise ValueError("Expected %s < %s" % (a, b))
            >>> MyContainer(1, 2)
            Traceback (most recent call last):
                ...
            ValueError: Missing value for 'field1'.

        WHAT !? Ok, lets write some more code::

            >>> MyContainer(field1=1, field2=2)
            Traceback (most recent call last):
                ...
            TypeError: __init__() ... arguments...

        This is banans. You have to write your class *around* these quirks.

    Lets try this::

        >>> class MyContainer(Fields.field1.field2):
        ...     def __init__(self, a, b):
        ...         if a > b:
        ...             raise ValueError("Expected %s < %s" % (a, b))
        ...         super(MyContainer, self).__init__(a, b)

    Just like a normal class, works as expected::

        >>> MyContainer(1, 2)
        <MyContainer(field1=1, field2=2)>

.. [*]

    Symbols should be symbols. The parity is remarcable - why validate strings so they are valid symbols when you can
    avoid that ? Just use symbols. Dooh !

    The use of language constructs is not that surprising - it's pretty obvious that in ``field2`` of ``field1`` of
    ``fields.Fields`` there *can't possibly be anything else but a class implementing a container for said two fields*.

    Why would anyone with a brain expect anything else ? It's like looking at a cake resembling a dog and expecting the
    cake to bark and run around.


Documentation
=============

https://python-fields.readthedocs.org/

Development
===========

To run the all tests run::

    tox
