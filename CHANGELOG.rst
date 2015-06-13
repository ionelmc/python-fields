
Changelog
=========

2.4.0 (2015-06-13)
------------------

* Similarly to ``fields.Fields``, added three new bases:

  * ``fields.BareFields`` (implements ``__init__``).
  * ``fields.ComparableMixin`` (implements ``__eq__``, ``__ne__``, ``__lt__``, ``__gt__``, ``__le__``, ``__ge__`` and ``__hash__``).
  * ``fields.PrintableMixin`` (implements ``__repr__``).

* Improved reference section in the docs.
* Added ``fields.ConvertibleFields`` and ``fields.ConvertibleMixin``. They have two convenience properties: ``as_dict`` and `as_tuple``.

2.3.0 (2015-01-20)
------------------

* Allowed overriding ``__slots__`` in ``SlotsFields`` subclasses.

2.2.0 (2015-01-19)
------------------

* Added ``make_init_func`` as an optional argument to ``class_sealer``. Rename the ``__base__`` option to just ``base``.

2.1.1 (2015-01-19)
------------------

* Removed bogus ``console_scripts`` entrypoint.

2.1.0 (2015-01-09)
------------------

* Added ``SlotsFields`` (same as ``Fields`` but automatically adds ``__slots__`` for memory efficiency on CPython).
* Added support for default argument to Tuple.

2.0.0 (2014-10-16)
------------------

* Made the __init__ in the FieldsBase way faster (used for ``fields.Fields``).
* Moved ``RegexValidate`` in ``fields.extras``.

1.0.0 (2014-10-05)
------------------

* Lots of internal changes, the metaclass is not created in a closure anymore. No more closures.
* Added ``RegexValidate`` container creator (should be taken as an example on using the Factory metaclass).
* Added support for using multiple containers as baseclasses.
* Added a ``super()`` `sink` so that ``super().__init__(*args, **kwargs)`` always works. Everything inherits from a
  baseclass that has an ``__init__`` that can take any argument (unlike ``object.__init__``). This allows for flexible
  usage.
* Added validation so that you can't use conflicting field layout when using multiple containers as the baseclass.
* Changed the __init__ function in the class container so it works like a python function w.r.t. positional and keyword
  arguments. Example: ``class MyContainer(Fields.a.b.c[1].d[2])`` will function the same way as ``def func(a, b, c=1,
  d=2)`` would when arguments are passed in. You can now use ``MyContainer(1, 2, 3, 4)`` (everything positional) or
  ``MyContainer(1, 2, 3, d=4)`` (mixed).

0.3.0 (2014-07-19)
------------------

* Corrected string repr.

0.2.0 (2014-06-28)
------------------

* Lots of breaking changes. Switched from __call__ to __getitem__ for default value assignment.

0.1.0 (2014-06-27)
------------------

* Alpha release.
