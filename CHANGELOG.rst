Changelog
=========

Versions follow `CalVer <http://calver.org>`_ with a strict backwards compatibility policy.
The third digit is only for regressions.


16.3.0 (2016-11-24)
-------------------

Changes:
^^^^^^^^

- Attributes now can have user-defined metadata which greatly improves ``attrs``'s extensibility.
  `#96 <https://github.com/hynek/attrs/pull/96>`_
- Allow for a ``__attrs_post_init__`` method that -- if defined -- will get called at the end of the ``attrs``-generated ``__init__`` method.
  `#111 <https://github.com/hynek/attrs/pull/111>`_
- Add ``@attr.s(str=True)`` that will optionally create a ``__str__`` method that is identical to ``__repr__``.
  This is mainly useful with ``Exception``\ s and other classes that rely on a useful ``__str__`` implementation but overwrite the default one through a poor own one.
  Default Python class behavior is to use ``__repr__`` as ``__str__`` anyways.

  If you tried using ``attrs`` with ``Exception``\ s and were puzzled by the tracebacks: this option is for you.
- Don't overwrite ``__name__`` with ``__qualname__`` for ``attr.s(slots=True)`` classes.
  `#99 <https://github.com/hynek/attrs/issues/99>`_


----


16.2.0 (2016-09-17)
-------------------

Changes:
^^^^^^^^

- Add ``attr.astuple()`` that -- similarly to ``attr.asdict()`` -- returns the instance as a tuple.
  `#77 <https://github.com/hynek/attrs/issues/77>`_
- Converts now work with frozen classes.
  `#76 <https://github.com/hynek/attrs/issues/76>`_
- Instantiation of ``attrs`` classes with converters is now significantly faster.
  `#80 <https://github.com/hynek/attrs/pull/80>`_
- Pickling now works with ``__slots__`` classes.
  `#81 <https://github.com/hynek/attrs/issues/81>`_
- ``attr.assoc()`` now works with ``__slots__`` classes.
  `#84 <https://github.com/hynek/attrs/issues/84>`_
- The tuple returned by ``attr.fields()`` now also allows to access the ``Attribute`` instances by name.
  Yes, we've subclassed ``tuple`` so you don't have to!
  Therefore ``attr.fields(C).x`` is equivalent to the deprecated ``C.x`` and works with ``__slots__`` classes.
  `#88 <https://github.com/hynek/attrs/issues/88>`_


----


16.1.0 (2016-08-30)
-------------------

Backward-incompatible changes:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- All instances where function arguments were called ``cl`` have been changed to the more Pythonic ``cls``.
  Since it was always the first argument, it's doubtful anyone ever called those function with in the keyword form.
  If so, sorry for any breakage but there's no practical deprecation path to solve this ugly wart.


Deprecations:
^^^^^^^^^^^^^

- Accessing ``Attribute`` instances on class objects is now deprecated and will stop working in 2017.
  If you need introspection please use the ``__attrs_attrs__`` attribute or the ``attr.fields()`` function that carry them too.
  In the future, the attributes that are defined on the class body and are usually overwritten in your ``__init__`` method are simply removed after ``@attr.s`` has been applied.

  This will remove the confusing error message if you write your own ``__init__`` and forget to initialize some attribute.
  Instead you will get a straightforward ``AttributeError``.
  In other words: decorated classes will work more like plain Python classes which was always ``attrs``'s goal.
- The serious business aliases ``attr.attributes`` and ``attr.attr`` have been deprecated in favor of ``attr.attrs`` and ``attr.attrib`` which are much more consistent and frankly obvious in hindsight.
  They will be purged from documentation immediately but there are no plans to actually remove them.


Changes:
^^^^^^^^

- ``attr.asdict()``\ 's ``dict_factory`` arguments is now propagated on recursion.
  `#45 <https://github.com/hynek/attrs/issues/45>`_
- ``attr.asdict()``, ``attr.has()`` and ``attr.fields()`` are significantly faster.
  `#48 <https://github.com/hynek/attrs/issues/48>`_
  `#51 <https://github.com/hynek/attrs/issues/51>`_
- Add ``attr.attrs`` and ``attr.attrib`` as a more consistent aliases for ``attr.s`` and ``attr.ib``.
- Add ``frozen`` option to ``attr.s`` that will make instances best-effort immutable.
  `#60 <https://github.com/hynek/attrs/issues/60>`_
- ``attr.asdict()`` now takes ``retain_collection_types`` as an argument.
  If ``True``, it does not convert attributes of type ``tuple`` or ``set`` to ``list``.
  `#69 <https://github.com/hynek/attrs/issues/69>`_


----


16.0.0 (2016-05-23)
-------------------

Backward-incompatible changes:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Python 3.3 and 2.6 aren't supported anymore.
  They may work by chance but any effort to keep them working has ceased.

  The last Python 2.6 release was on October 29, 2013 and isn't supported by the CPython core team anymore.
  Major Python packages like Django and Twisted dropped Python 2.6 a while ago already.

  Python 3.3 never had a significant user base and wasn't part of any distribution's LTS release.

Changes:
^^^^^^^^

- ``__slots__`` have arrived!
  Classes now can automatically be `slots <https://docs.python.org/3.5/reference/datamodel.html#slots>`_-style (and save your precious memory) just by passing ``slots=True``.
  `#35 <https://github.com/hynek/attrs/issues/35>`_
- Allow the case of initializing attributes that are set to ``init=False``.
  This allows for clean initializer parameter lists while being able to initialize attributes to default values.
  `#32 <https://github.com/hynek/attrs/issues/32>`_
- ``attr.asdict()`` can now produce arbitrary mappings instead of Python ``dict``\ s when provided with a ``dict_factory`` argument.
  `#40 <https://github.com/hynek/attrs/issues/40>`_
- Multiple performance improvements.


----


15.2.0 (2015-12-08)
-------------------

Changes:
^^^^^^^^

- Add a ``convert`` argument to ``attr.ib``, which allows specifying a function to run on arguments.
  This allows for simple type conversions, e.g. with ``attr.ib(convert=int)``.
  `#26 <https://github.com/hynek/attrs/issues/26>`_
- Speed up object creation when attribute validators are used.
  `#28 <https://github.com/hynek/attrs/issues/28>`_


----


15.1.0 (2015-08-20)
-------------------

Changes:
^^^^^^^^

- Add ``attr.validators.optional`` that wraps other validators allowing attributes to be ``None``.
  `#16 <https://github.com/hynek/attrs/issues/16>`_
- Fix multi-level inheritance.
  `#24 <https://github.com/hynek/attrs/issues/24>`_
- Fix ``__repr__`` to work for non-redecorated subclasses.
  `#20 <https://github.com/hynek/attrs/issues/20>`_


----


15.0.0 (2015-04-15)
-------------------

Changes:
^^^^^^^^

Initial release.
