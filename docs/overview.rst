========
Overview
========

In order to fullfil its ambitious goal of bringing back the joy to writing classes, it gives you a class decorator and a way to declaratively define the attributes on that class:

.. include:: ../README.rst
   :start-after: -code-begin-
   :end-before: -testimonials-


What ``attrs`` Is Not
=====================

``attrs`` does *not* invent some kind of magic system that pulls classes out of its hat using meta classes, runtime introspection, and shaky interdependencies.

All ``attrs`` does is take your declaration, write dunder methods based on that information, and attach them to your class.
It does *nothing* dynamic at runtime, hence zero runtime overhead.
It's still *your* class.
Do with it as you please.


On the ``attr.s`` and ``attr.ib`` Names
=======================================

The ``attr.s`` decorator and the ``attr.ib`` function aren't any obscure abbreviations.
They are a *concise* and highly *readable* way to write ``attrs`` and ``attrib`` with an *explicit namespace*.

At first, some people have a negative gut reaction to that; resembling the reactions to Python's significant whitespace.
And as with that, once one gets used to it, the readability and explicitness of that API prevails and delights.

For those who can't swallow that API at all, ``attrs`` comes with serious business aliases: ``attr.attrs`` and ``attr.attrib``.

Therefore, the following class definition is identical to the previous one:

.. doctest::

   >>> from attr import attrs, attrib, Factory
   >>> @attrs
   ... class C(object):
   ...     x = attrib(default=42)
   ...     y = attrib(default=Factory(list))
   >>> C()
   C(x=42, y=[])

Use whichever variant fits your taste better.
