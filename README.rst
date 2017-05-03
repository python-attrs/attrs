.. image:: http://www.attrs.org/en/latest/_static/attrs_logo.png
   :alt: attrs Logo

==================================
attrs: Classes Without Boilerplate
==================================

.. image:: https://readthedocs.org/projects/attrs/badge/?version=stable
   :target: http://www.attrs.org/en/stable/?badge=stable
   :alt: Documentation Status

.. image:: https://travis-ci.org/python-attrs/attrs.svg?branch=master
   :target: https://travis-ci.org/python-attrs/attrs
   :alt: CI Status

.. image:: https://codecov.io/github/python-attrs/attrs/branch/master/graph/badge.svg
   :target: https://codecov.io/github/python-attrs/attrs
   :alt: Test Coverage

.. teaser-begin

``attrs`` is the Python package that will bring back the **joy** of **writing classes** by relieving you from the drudgery of implementing object protocols (aka `dunder <https://nedbatchelder.com/blog/200605/dunder.html>`_ methods).

Its main goal is to help you to write **concise** and **correct** software without slowing down your code.

.. -spiel-end-

For that, it gives you a class decorator and a way to declaratively define the attributes on that class:

.. -code-begin-

.. code-block:: pycon

   >>> import attr
   >>> @attr.s
   ... class Point(object):
   ...     x = attr.ib(default=42)
   ...     y = attr.ib(default=attr.Factory(list))
   ...
   ...     def hard_math(self, z):
   ...         return self.x * self.y * z
   >>> pt = Point(x=1, y=2)
   >>> pt
   Point(x=1, y=2)
   >>> pt.hard_math(3)
   6
   >>> pt == Point(1, 2)
   True
   >>> pt != Point(2, 1)
   True
   >>> attr.asdict(pt)
   {'x': 1, 'y': 2}
   >>> Point()
   Point(x=42, y=[])
   >>> C = attr.make_class("C", ["a", "b"])
   >>> C("foo", "bar")
   C(a='foo', b='bar')


After *declaring* your attributes ``attrs`` gives you:

- a concise and explicit overview of the class's attributes,
- a nice human-readable ``__repr__``,
- a complete set of comparison methods,
- an initializer,
- and much more,

*without* writing dull boilerplate code again and again and *without* runtime performance penalties.

This gives you the power to use actual classes with actual types in your code instead of confusing ``tuple``\ s or confusingly behaving ``namedtuple``\ s.
Which in turn encourages you to write *small classes* that do `one thing well <https://www.destroyallsoftware.com/talks/boundaries>`_.
Never again violate the `single responsibility principle <https://en.wikipedia.org/wiki/Single_responsibility_principle>`_ just because implementing ``__init__`` et al is a painful drag.


.. -testimonials-

Testimonials
============

  I’m looking forward to is being able to program in Python-with-attrs everywhere.
  It exerts a subtle, but positive, design influence in all the codebases I’ve see it used in.

  -- Glyph Lefkowitz, creator of `Twisted <https://twistedmatrix.com/>`_ and Software Developer at Rackspace in `The One Python Library Everyone Needs <https://glyph.twistedmatrix.com/2016/08/attrs.html>`_


  I'm increasingly digging your attr.ocity. Good job!

  -- Łukasz Langa, prolific CPython core developer and Production Engineer at Facebook


  Writing a fully-functional class using ``attrs`` takes me less time than writing this testimonial.

  -- Amber Hawkie Brown, Twisted Release Manager and Computer Owl


.. -end-

.. -project-information-

Project Information
===================

``attrs`` is released under the `MIT <https://choosealicense.com/licenses/mit/>`_ license,
its documentation lives at `Read the Docs <http://www.attrs.org/>`_,
the code on `GitHub <https://github.com/python-attrs/attrs>`_,
and the latest release on `PyPI <https://pypi.org/project/attrs/>`_.
It’s rigorously tested on Python 2.7, 3.4+, and PyPy.

If you'd like to contribute you're most welcome and we've written `a little guide <http://www.attrs.org/en/latest/contributing.html>`_ to get you started!
