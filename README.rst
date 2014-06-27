===============================
python-fields
===============================

.. image:: http://img.shields.io/travis/ionelmc/python-fields/master.png
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-fields

.. See: http://www.appveyor.com/docs/status-badges

.. image:: https://ci.appveyor.com/api/projects/status/<security-token>/branch/master
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

An example package. Replace this with a proper project description. Generated with https://github.com/ionelmc/cookiecutter-pylibrary

* Free software: BSD license

Installation
============

::

    pip install fields

Usage
=====

::

    >>> from fields import Fields
    >>>
    >>> class Pair(Fields.a.b):
    ...     pass
    ...
    >>> p = Pair(1, 2)
    >>> p.a
    1
    >>> p.b
    2
    >>> class Node(Fields.value.left(None).right(None)):
    ...     pass
    ...
    >>> p = Node(1, left=Node(2), right=Node(3, left=Node(4)))
    >>> p
    <Node(left=<Node(left=None, right=None, value=2)>, right=<Node(left=<Node(left=None, right=None, value=4)>, right=None, value=3)>, value=1)>

Documentation
=============

https://python-fields.readthedocs.org/

Development
===========

To run the all tests run::

    tox
