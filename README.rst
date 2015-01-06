===============================
        python-fields
===============================

| |docs| |travis| |appveyor| |coveralls| |landscape| |scrutinizer|
| |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-fields/badge/?style=flat
    :target: https://readthedocs.org/projects/python-fields
    :alt: Documentation Status

.. |travis| image:: http://img.shields.io/travis/ionelmc/python-fields/master.png?style=flat
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-fields

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/python-fields?branch=master
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-fields

.. |coveralls| image:: http://img.shields.io/coveralls/ionelmc/python-fields/master.png?style=flat
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-fields

.. |landscape| image:: https://landscape.io/github/ionelmc/python-fields/master/landscape.svg?style=flat
    :target: https://landscape.io/github/ionelmc/python-fields/master
    :alt: Code Quality Status

.. |version| image:: http://img.shields.io/pypi/v/fields.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/fields

.. |downloads| image:: http://img.shields.io/pypi/dm/fields.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/fields

.. |wheel| image:: https://pypip.in/wheel/fields/badge.png?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/fields

.. |supported-versions| image:: https://pypip.in/py_versions/fields/badge.png?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/fields

.. |supported-implementations| image:: https://pypip.in/implementation/fields/badge.png?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/fields

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/ionelmc/python-fields/master.png?style=flat
    :alt: Scrtinizer Status
    :target: https://scrutinizer-ci.com/g/ionelmc/python-fields/

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

Usage & examples
================

A class that has 2 attributes, ``a`` and ``b``:

.. code:: python

    >>> from fields import Fields
    >>> class Pair(Fields.a.b):
    ...     pass
    ...
    >>> p = Pair(1, 2)
    >>> p.a
    1
    >>> p.b
    2
    >>> Pair(a=1, b=2)
    Pair(a=1, b=2)

A class that has one required attribute ``value`` and two attributes (``left`` and ``right``) with default value
``None``:

.. code:: python

    >>> class Node(Fields.value.left[None].right[None]):
    ...     pass
    ...
    >>> Node(1, Node(2), Node(3, Node(4)))
    Node(value=1, left=Node(value=2, left=None, right=None), right=Node(value=3, left=Node(value=4, left=None, right=None), right=None))
    >>> Node(1, right=Node(2))
    Node(value=1, left=None, right=Node(value=2, left=None, right=None))


Want tuples?
------------

An alternative to ``namedtuple``:

.. code:: python

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

Documentation
=============

https://python-fields.readthedocs.org/

Development
===========

To run all the tests run ``tox`` in your shell (``pip install tox`` if you don't have it)::

    tox

FAQ
===

Why should I use this?
-----------------------

It's less to type, why have quotes around when the names need to be valid symbols anyway. In fact, this is one of the
shortest forms possible to specify a container with fields.

But you're abusing a very well known syntax. You're using attribute access instead of a list of strings. Why?
--------------------------------------------------------------------------------------------------------------

Symbols should be symbols. Why validate strings so they are valid symbols when you can avoid that? Just use symbols.
Save on both typing and validation code.

The use of language constructs is not that surprising or confusing in the sense that semantics precede conventional
syntax use. For example, if we have ``class Person(Fields.first_name.last_name.height.weight): pass`` then it's going to
be clear we're talking about a *Person* object with *first_name*, *last_name*, *height* and *width* fields: the words
have clear meaning.

Again, you should not name your varibles as `f1`, `f2` or any other non-semantic symbols anyway.

Semantics precede syntax: it's like looking at a cake resembling a dog, you won't expect the cake to bark and run
around.

Is this stable? Is it tested?
-------------------------------

Yes. Mercilessly tested on `Travis <https://travis-ci.org/ionelmc/python-fields>`_ and `AppVeyor
<https://ci.appveyor.com/project/ionelmc/python-fields>`_.

Is the API stable?
-------------------

Yes, ofcourse.

Why not ``namedtuple``?
------------------------

It's ugly, repetivive and unflexible. Compare this:

.. code:: python

    >>> from collections import namedtuple
    >>> class MyContainer(namedtuple("MyContainer", ["field1", "field2"])):
    ...     pass
    >>> MyContainer(1, 2)
    MyContainer(field1=1, field2=2)

To this:

.. code:: python

    >>> class MyContainer(Tuple.field1.field2):
    ...     pass
    >>> MyContainer(1, 2)
    MyContainer(field1=1, field2=2)

Why not ``characteristic``?
----------------------------

Ugly, inconsistent - you don't own the class:

    Lets try this:

    .. code:: python

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

    WHAT !? Ok, lets write some more code:

    .. code:: python

        >>> MyContainer(field1=1, field2=2)
        Traceback (most recent call last):
            ...
        TypeError: __init__() ... arguments...

    This is bananas. You have to write your class *around* these quirks.

Lets try this:

.. code:: python

    >>> class MyContainer(Fields.field1.field2):
    ...     def __init__(self, a, b):
    ...         if a > b:
    ...             raise ValueError("Expected %s < %s" % (a, b))
    ...         super(MyContainer, self).__init__(a, b)

Just like a normal class, works as expected:

.. code:: python

    >>> MyContainer(1, 2)
    MyContainer(field1=1, field2=2)


Won't this confuse ``pylint``?
------------------------------

Normaly it would, but there's a plugin that makes pylint understand it, just like any other class:
`pylint-fields <https://github.com/ionelmc/pylint-fields>`_.
