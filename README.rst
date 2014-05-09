characteristic
==============

.. image:: https://travis-ci.org/hynek/characteristic.svg
   :target: https://travis-ci.org/hynek/characteristic

.. image:: https://coveralls.io/repos/hynek/characteristic/badge.png?branch=master
    :target: https://coveralls.io/r/hynek/characteristic?branch=master

`characteristic` is an MIT_-licensed package that eases the chores of implementing certain attribute-related object protocols in Python.
It’s inspired by Twisted’s `FancyEqMixin`_ but is implemented using class decorators because `sub-classing is bad for you`_, m’kay\ [*]_?

It’s continuously tested on Python 2.6, 2.7, 3.3, 3.4, and PyPy.

.. [*] Just look at FancyEqMixin_\’s list of known subclasses and weep.


Examples
--------



.. _FancyEqMixin: http://twistedmatrix.com/documents/current/api/twisted.python.util.FancyEqMixin.html
.. _`sub-classing is bad for you`: https://www.youtube.com/watch?v=3MNVP9-hglc
.. _MIT: http://choosealicense.com/licenses/mit/
