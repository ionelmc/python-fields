======
Fields
======

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-fields/badge/?style=flat
    :target: https://readthedocs.org/projects/python-fields
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/ionelmc/python-fields.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-fields

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/python-fields?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-fields

.. |requires| image:: https://requires.io/github/ionelmc/python-fields/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/python-fields/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/ionelmc/python-fields/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-fields

.. |codecov| image:: https://codecov.io/github/ionelmc/python-fields/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-fields

.. |landscape| image:: https://landscape.io/github/ionelmc/python-fields/master/landscape.svg?style=flat
    :target: https://landscape.io/github/ionelmc/python-fields/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg?style=flat
    :target: https://www.codacy.com/app/ionelmc/python-fields
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/ionelmc/python-fields/badges/gpa.svg
   :target: https://codeclimate.com/github/ionelmc/python-fields
   :alt: CodeClimate Quality Status
.. |version| image:: https://img.shields.io/pypi/v/fields.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/fields

.. |downloads| image:: https://img.shields.io/pypi/dm/fields.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/fields

.. |wheel| image:: https://img.shields.io/pypi/wheel/fields.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/fields

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/fields.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/fields

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/fields.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/fields

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/ionelmc/python-fields/master.svg?style=flat
    :alt: Scrutinizer Status
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

.. code:: pycon

    >>> from fields import Fields
    >>> class Pizza(Fields.name.size):
    ...     pass
    ...
    >>> p = Pizza("Pepperoni", "large")
    >>> p
    Pizza(name='Pepperoni', size='large')
    >>> p.size
    'large'
    >>> p.name
    'Pepperoni'

You can also use keyword arguments:

.. code:: pycon

    >>> Pizza(size="large", name="Pepperoni")
    Pizza(name='Pepperoni', size='large')

You can have as many attributes as you want:

.. code:: pycon

    >>> class Pizza(Fields.name.ingredients.crust.size):
    ...     pass
    ...
    >>> Pizza("Funghi", ["mushrooms", "mozarella"], "thin", "large")
    Pizza(name='Funghi', ingredients=['mushrooms', 'mozarella'], crust='thin', size='large')


A class that has one required attribute ``value`` and two attributes (``left`` and ``right``) with default value
``None``:

.. code:: pycon

    >>> class Node(Fields.value.left[None].right[None]):
    ...     pass
    ...
    >>> Node(1, Node(2), Node(3, Node(4)))
    Node(value=1, left=Node(value=2, left=None, right=None), right=Node(value=3, left=Node(value=4, left=None, right=None), right=None))
    >>> Node(1, right=Node(2))
    Node(value=1, left=None, right=Node(value=2, left=None, right=None))

You can also use it *inline*:

.. code:: pycon

    >>> Fields.name.size("Pepperoni", "large")
    FieldsBase(name='Pepperoni', size='large')

Want tuples?
------------

An alternative to ``namedtuple``:

.. code:: python

    >>> from fields import Tuple
    >>> class Pair(Tuple.a.b):
    ...     pass
    ...
    >>> issubclass(Pair, tuple)
    True
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

Tuples are *fast*!

::

    benchmark: 9 tests, min 5 rounds (of min 25.00us), 1.00s max time, timer: time.perf_counter

    Name (time in us)                 Min        Max     Mean   StdDev  Rounds  Iterations
    --------------------------------------------------------------------------------------
    test_characteristic            6.0100  1218.4800  11.7102  34.3158   15899          10
    test_fields                    6.8000  1850.5250   9.8448  33.8487    5535           4
    test_slots_fields              6.3500   721.0300   8.6120  14.8090   15198          10
    test_super_dumb                7.0111  1289.6667  11.6881  31.6012   15244           9
    test_dumb                      3.7556   673.8444   5.8010  15.0514   14246          18
    test_tuple                     3.1750   478.7750   5.1974   9.1878   14642          12
    test_namedtuple                3.2778   538.1111   5.0403   9.9177   14105           9
    test_attrs_decorated_class     4.2062   540.5125   5.3618  11.6708   14266          16
    test_attrs_class               3.7889   316.1056   4.7731   6.0656   14026          18
    --------------------------------------------------------------------------------------

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
----------------------

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

Again, you should not name your variables as `f1`, `f2` or any other non-semantic symbols anyway.

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

Why not ``attrs``?
------------------

Now this is a very difficult question.

Consider this typical use-case::

.. sourcecode:: pycon

    >>> import attr
    >>> @attr.s
    ... class Point(object):
    ...     x = attr.ib()
    ...     y = attr.ib()

Worth noting:

* attrs_ is faster because it doesn't allow your class to be
  used as a mixin (it doesn't do any ``super(cls, self).__init__(...)`` for you).
* the typical use-case doesn't allow you to have a custom ``__init__``. If you define a custom
  ``__init__``, it will get overridden by the one attrs_ generates.
* It works better with IDEs and source code analysis tools because of the
  attributes defined on the class.

All in all, attrs_ is a fast and minimal container library with no support for
subclasses. Definitely worth considering.

.. _attrs: <https://pypi.python.org/pypi/attrs

Won't this confuse ``pylint``?
------------------------------

Normaly it would, but there's a plugin that makes pylint understand it, just like any other class:
`pylint-fields <https://github.com/ionelmc/pylint-fields>`_.
