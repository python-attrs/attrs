characteristic: Say 'yes' to types but 'no' to typing!
======================================================

Release v\ |release| (:doc:`What's new? <changelog>`).


.. include:: ../README.rst
   :start-after: begin


Teaser
------

.. doctest::

   >>> from characteristic import Attribute, attributes
   >>> @attributes
   ... class AClass(object):
   ...     a = Attribute()
   ...     b = Attribute()
   >>> @attributes
   ... class AnotherClass(object):
   ...     a = Attribute()
   ...     b = Attribute(default="abc")
   >>> obj1 = AClass(a=1, b="abc")
   >>> obj2 = AnotherClass(a=1, b="abc")
   >>> obj3 = AnotherClass(a=1)
   >>> print obj1, obj2, obj3
   <AClass(a=1, b='abc')> <AnotherClass(a=1, b='abc')> <AnotherClass(a=1, b='abc')>
   >>> obj1 == obj2
   False
   >>> obj2 == obj3
   True


User's Guide
------------

.. toctree::
   :maxdepth: 1

   why
   api
   examples

Project Information
^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   license
   contributing
   changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
