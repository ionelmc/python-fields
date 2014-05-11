characteristic: Say ‘yes’ to types but ‘no’ to typing!
======================================================

.. image:: https://travis-ci.org/hynek/characteristic.svg
   :target: https://travis-ci.org/hynek/characteristic

.. image:: https://coveralls.io/repos/hynek/characteristic/badge.png?branch=master
    :target: https://coveralls.io/r/hynek/characteristic?branch=master

.. begin


``characteristic`` is an `MIT <http://choosealicense.com/licenses/mit/>`_-licensed Python package with class decorators that ease the chores of implementing the most common attribute-related object protocols.

You just specify the attributes to work with and ``characteristic`` gives you:

- a nice human-readable ``__repr__``,
- a complete set of comparison methods,
- and a kwargs-based initializer (that cooperates with your existing one)

*without* writing dull boilerplate code again and again.

So put down that type-less data structures and welcome some class into your life!

``characteristic``\ ’s documentation lives at `Read the Docs <https://characteristic.readthedocs.org/>`_, the code on `GitHub <https://github.com/hynek/characteristic>`_.
It’s rigorously tested on Python 2.6, 2.7, 3.3+, and PyPy.
