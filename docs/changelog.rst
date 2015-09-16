.. currentmodule:: attr

.. :changelog:

Changelog
=========

Versions are year-based with a strict :doc:`backwards-compatibility policy <backward-compatibility>`.
The third digit is only for regressions.


15.2.0 (UNRELEASED)
-------------------


Changes:
^^^^^^^^

- Add a `convert` argument to :func:`attr.ib`, which allows specifying a function to run on arguments.  This allows for simple type conversions, e.g. with ``attr.ib(convert=int)``. `[26] <https://github.com/hynek/attrs/issues/26>`
- speed up object creation when attribute validators are used `[28] <https://github.com/hynek/attrs/issues/28>`_


15.1.0 (2015-08-20)
-------------------


Changes:
^^^^^^^^

- Add :func:`attr.validators.optional` that wraps other validators allowing attributes to be ``None``. `[16] <https://github.com/hynek/attrs/issues/16>`_
- Fix multi-level inheritance. `[24] <https://github.com/hynek/attrs/issues/24>`_
- Fix ``__repr__`` to work for non-redecorated subclasses. `[20] <https://github.com/hynek/attrs/issues/20>`_


15.0.0 (2015-04-15)
-------------------


Changes:
^^^^^^^^

- Initial release.
