======================================
attrs: Attributes without boilerplate.
======================================

.. image:: https://readthedocs.org/projects/attrs/badge/?version=stable
   :target: http://attrs.readthedocs.io/en/stable/?badge=stable
   :alt: Documentation Status

.. image:: https://travis-ci.org/hynek/attrs.svg
   :target: https://travis-ci.org/hynek/attrs
   :alt: CI status

.. image:: https://codecov.io/github/hynek/attrs/coverage.svg?branch=master
   :target: https://codecov.io/github/hynek/attrs?branch=master
   :alt: Coverage

.. teaser-begin

``attrs`` is an `MIT <http://choosealicense.com/licenses/mit/>`_-licensed Python package with class decorators that ease the chores of implementing the most common attribute-related object protocols:

.. code-block:: pycon

   >>> import attr
   >>> @attr.s
   ... class C(object):
   ...     x = attr.ib(default=42)
   ...     y = attr.ib(default=attr.Factory(list))
   >>> i = C(x=1, y=2)
   >>> i
   C(x=1, y=2)
   >>> i == C(1, 2)
   True
   >>> i != C(2, 1)
   True
   >>> attr.asdict(i)
   {'y': 2, 'x': 1}
   >>> C()
   C(x=42, y=[])
   >>> C2 = attr.make_class("C2", ["a", "b"])
   >>> C2("foo", "bar")
   C2(a='foo', b='bar')

(If you don’t like the playful ``attr.s`` and ``attr.ib``, you can also use their no-nonsense aliases ``attr.attributes`` and ``attr.attr``).

You just specify the attributes to work with and ``attrs`` gives you:

- a nice human-readable ``__repr__``,
- a complete set of comparison methods,
- an initializer,
- and much more

*without* writing dull boilerplate code again and again.

This gives you the power to use actual classes with actual types in your code instead of confusing ``tuple``\ s or confusingly behaving ``namedtuple``\ s.

So put down that type-less data structures and welcome some class into your life!

``attrs``\ ’s documentation lives at `Read the Docs <https://attrs.readthedocs.io/>`_, the code on `GitHub <https://github.com/hynek/attrs>`_.
It’s rigorously tested on Python 2.7, 3.4+, and PyPy.
