=============================================
attrs: Python attributes without boilerplate.
=============================================

.. image:: https://pypip.in/version/attrs/badge.svg
   :target: https://pypi.python.org/pypi/attrs/
   :alt: Latest Version

.. image:: https://travis-ci.org/hynek/attrs.svg
   :target: https://travis-ci.org/hynek/attrs
   :alt: CI status

.. image:: https://coveralls.io/repos/hynek/attrs/badge.png?branch=master
   :target: https://coveralls.io/r/hynek/attrs?branch=master
   :alt: Current coverage

.. begin

``attrs`` is an `MIT <http://choosealicense.com/licenses/mit/>`_-licensed Python package with class decorators that ease the chores of implementing the most common attribute-related object protocols:

.. code-block:: pycon

   >>> import attr
   >>> @attr.s
   ... class C(object):
   ...     x = attr.a(default_value=42)
   ...     y = attr.a(default_factory=list)
   >>> i = C(x=1, y=2)
   >>> i
   <C(x=1, y=2)>
   >>> i == C(1, 2)
   True
   >>> i != C(2, 1)
   True
   >>> attr.to_dict(i)
   {'y': 2, 'x': 1}
   >>> C()
   <C(x=42, y=[])>

You just specify the attributes to work with and ``attrs`` gives you:

- a nice human-readable ``__repr__``,
- a complete set of comparison methods,
- and an initializer

*without* writing dull boilerplate code again and again.

This gives you the power to use actual classes with actual types in your code instead of confusing ``tuple``\ s or confusingly behaving ``namedtuple``\ s.

So put down that type-less data structures and welcome some class into your life!

``attrs``\ ’s documentation lives at `Read the Docs <https://attrs.readthedocs.org/>`_, the code on `GitHub <https://github.com/hynek/attrs>`_.
It’s rigorously tested on Python 2.6, 2.7, 3.3+, and PyPy.
