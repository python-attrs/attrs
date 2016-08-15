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

If you don’t like the playful ``attr.s`` and ``attr.ib`` (that aren't any obscure abbreviations; just a concise and highly readable way to write ``attrs`` and ``attrib`` with an explicit namespace), ``attrs`` comes with no-nonsense aliases: ``attr.attributes`` and ``attr.attr``.
Sometimes it takes a few minutes to get used to the short forms, but in the long run, they're more readable and therefore grokkable when reading code.

After *declaring* your attributes ``attrs`` gives you:

- a concise and explicit overview of the class's attributes,
- a nice human-readable ``__repr__``,
- a complete set of comparison methods,
- an initializer,
- and much more

*without* writing dull boilerplate code again and again and *without* runtime performance penalties.

This gives you the power to use actual classes with actual types in your code instead of confusing ``tuple``\ s or confusingly behaving ``namedtuple``\ s.
Which in turn encourages you to write *small classes* that do `one thing well <https://www.destroyallsoftware.com/talks/boundaries>`_.
Never again violate the `single responsibility principle <https://en.wikipedia.org/wiki/Single_responsibility_principle>`_ just because implementing ``__init__`` et al is a painful drag.

``attrs``\ 's main objective is to help you to write *concise* and *correct* software without slowing you down.


What ``attrs`` Is Not
=====================

``attrs`` does *not* invent some kind of magic system that pulls classes out of its hat using meta classes, runtime introspection, and shaky interdependencies.

All ``attrs`` does is taking your declaration, writing dunder methods based on that information, and attaching them to your class.
It does *nothing* dynamic at runtime, hence zero runtime overhead.
It's still *your* class.
Do with it as you please.


Testimonials
============

  I’m looking forward to is being able to program in Python-with-attrs everywhere.
  It exerts a subtle, but positive, design influence in all the codebases I’ve see it used in.

  -- Glyph Lefkowitz, inventor of Twisted and Software Developer at Rackspace in `The One Python Library Everyone Needs <https://glyph.twistedmatrix.com/2016/08/attrs.html>`_


  I'm increasingly digging your attr.ocity. Good job!

  -- Łukasz Langa, prolific CPython core developer and Production Engineer at Facebook

.. -end-


Project Information
===================

``attrs``\ ’s documentation lives at `Read the Docs <https://attrs.readthedocs.io/>`_, and the code on `GitHub <https://github.com/hynek/attrs>`_.
It’s rigorously tested on Python 2.7, 3.4+, and PyPy.
