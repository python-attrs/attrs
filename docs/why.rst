.. _why:

Why not…
========


If you'd like third party's account why ``attrs`` is great, have a look at Glyph's `The One Python Library Everyone Needs <https://glyph.twistedmatrix.com/2016/08/attrs.html>`_!


…tuples?
--------


Readability
^^^^^^^^^^^

What makes more sense while debugging::

   Point(x=1, y=2)

or::

   (1, 2)

?

Let's add even more ambiguity::

   Customer(id=42, reseller=23, first_name="Jane", last_name="John")

or::

   (42, 23, "Jane", "John")

?

Why would you want to write ``customer[2]`` instead of ``customer.first_name``?

Don't get me started when you add nesting.
If you've never ran into mysterious tuples you had no idea what the hell they meant while debugging, you're much smarter then I am.

Using proper classes with names and types makes program code much more readable and comprehensible_.
Especially when trying to grok a new piece of software or returning to old code after several months.

.. _comprehensible: https://arxiv.org/pdf/1304.5257.pdf


Extendability
^^^^^^^^^^^^^

Imagine you have a function that takes or returns a tuple.
Especially if you use tuple unpacking (eg. ``x, y = get_point()``), adding additional data means that you have to change the invocation of that function *everywhere*.

Adding an attribute to a class concerns only those who actually care about that attribute.


…namedtuples?
-------------

The difference between :func:`collections.namedtuple`\ s and classes decorated by ``attrs`` is that the latter are type-sensitive and require less typing as compared with regular classes:


.. doctest::

   >>> import attr
   >>> @attr.s
   ... class C1(object):
   ...     a = attr.ib()
   ...     def print_a(self):
   ...        print(self.a)
   >>> @attr.s
   ... class C2(object):
   ...     a = attr.ib()
   >>> c1 = C1(a=1)
   >>> c2 = C2(a=1)
   >>> c1.a == c2.a
   True
   >>> c1 == c2
   False
   >>> c1.print_a()
   1


…while a namedtuple is *explicitly* intended to behave like a tuple:


.. doctest::

   >>> from collections import namedtuple
   >>> NT1 = namedtuple("NT1", "a")
   >>> NT2 = namedtuple("NT2", "b")
   >>> t1 = NT1._make([1,])
   >>> t2 = NT2._make([1,])
   >>> t1 == t2 == (1,)
   True


This can easily lead to surprising and unintended behaviors.

Additionally, classes decorated with ``attrs`` can be either mutable or immutable.
Immutable classes are created by simply passing a ``frozen=True`` argument to the ``attrs`` decorator, as described in the :doc:`api`.
By default, however, classes created by ``attrs`` are mutable:

.. doctest::

   >>> import attr
   >>> @attr.s
   ... class Customer(object):
   ...     first_name = attr.ib()
   >>> c1 = Customer(first_name='Kaitlyn')
   >>> c1.first_name
   'Kaitlyn'
   >>> c1.first_name = 'Katelyn'
   >>> c1.first_name
   'Katelyn'

…while classes created with :func:`collections.namedtuple` inherit from tuple and are therefore always immutable:

.. doctest::

   >>> from collections import namedtuple
   >>> Customer = namedtuple('Customer', 'first_name')
   >>> c1 = Customer(first_name='Kaitlyn')
   >>> c1.first_name
   'Kaitlyn'
   >>> c1.first_name = 'Katelyn'
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   AttributeError: can't set attribute

Other than that, ``attrs`` also adds nifty features like validators and default values.

.. _tuple: https://docs.python.org/2/tutorial/datastructures.html#tuples-and-sequences


…dicts?
-------

Dictionaries are not for fixed fields.

If you have a dict, it maps something to something else.
You should be able to add and remove values.

Objects, on the other hand, are supposed to have specific fields of specific types, because their methods have strong expectations of what those fields and types are.

``attrs`` lets you be specific about those expectations; a dictionary does not.
It gives you a named entity (the class) in your code, which lets you explain in other places whether you take a parameter of that class or return a value of that class.

In other words: if your dict has a fixed and known set of keys, it is an object, not a hash.


…hand-written classes?
----------------------

While I'm a fan of all things artisanal, writing the same nine methods all over again doesn't qualify for me.
I usually manage to get some typos inside and there's simply more code that can break and thus has to be tested.

To bring it into perspective, the equivalent of

.. doctest::

   >>> @attr.s
   ... class SmartClass(object):
   ...    a = attr.ib()
   ...    b = attr.ib()
   >>> SmartClass(1, 2)
   SmartClass(a=1, b=2)

is

.. doctest::

   >>> class ArtisanalClass(object):
   ...     def __init__(self, a, b):
   ...         self.a = a
   ...         self.b = b
   ...
   ...     def __repr__(self):
   ...         return "ArtisanalClass(a={}, b={})".format(self.a, self.b)
   ...
   ...     def __eq__(self, other):
   ...         if other.__class__ is self.__class__:
   ...             return (self.a, self.b) == (other.a, other.b)
   ...         else:
   ...             return NotImplemented
   ...
   ...     def __ne__(self, other):
   ...         result = self.__eq__(other)
   ...         if result is NotImplemented:
   ...             return NotImplemented
   ...         else:
   ...             return not result
   ...
   ...     def __lt__(self, other):
   ...         if other.__class__ is self.__class__:
   ...             return (self.a, self.b) < (other.a, other.b)
   ...         else:
   ...             return NotImplemented
   ...
   ...     def __le__(self, other):
   ...         if other.__class__ is self.__class__:
   ...             return (self.a, self.b) <= (other.a, other.b)
   ...         else:
   ...             return NotImplemented
   ...
   ...     def __gt__(self, other):
   ...         if other.__class__ is self.__class__:
   ...             return (self.a, self.b) > (other.a, other.b)
   ...         else:
   ...             return NotImplemented
   ...
   ...     def __ge__(self, other):
   ...         if other.__class__ is self.__class__:
   ...             return (self.a, self.b) >= (other.a, other.b)
   ...         else:
   ...             return NotImplemented
   ...
   ...     def __hash__(self):
   ...         return hash((self.a, self.b))
   >>> ArtisanalClass(a=1, b=2)
   ArtisanalClass(a=1, b=2)

which is quite a mouthful and it doesn't even use any of ``attrs``'s more advanced features like validators or defaults values.
Also: no tests whatsoever.
And who will guarantee you, that you don't accidentally flip the ``<`` in your tenth implementation of ``__gt__``?

If you don't care and like typing, I'm not gonna stop you.
But if you ever get sick of the repetitiveness, ``attrs`` will be waiting for you. :)


…characteristic?
----------------

`characteristic <https://characteristic.readthedocs.io/>`_ is a very similar and fairly popular project of mine.
So why the self-fork?
Basically after nearly a year of usage I ran into annoyances and regretted certain decisions I made early-on to make too many people happy.
In the end, *I* wasn't happy using it anymore.

So I learned my lesson and ``attrs`` is the result of that.


Reasons For Forking
^^^^^^^^^^^^^^^^^^^

- Fixing those aforementioned annoyances would introduce more complexity.
  More complexity means more bugs.
- Certain unused features make other common features complicated or impossible.
  Prime example is the ability write your own initializers and make the generated one cooperate with it.
  The new logic is much simpler allowing for writing optimal initializers.
- I want it to be possible to gradually move from ``characteristic`` to ``attrs``.
  A peaceful co-existence is much easier if it's separate packages altogether.
- My libraries have very strict backward-compatibility policies and it would take years to get rid of those annoyances while they shape the implementation of other features.
- The name is tooo looong.


Main Differences
^^^^^^^^^^^^^^^^

- The attributes are defined *within* the class definition such that code analyzers know about their existence.
  This is useful in IDEs like PyCharm or linters like PyLint.
  ``attrs``'s classes look much more idiomatic than ``characteristic``'s.
  Since it's useful to use ``attrs`` with classes you don't control (e.g. Django models), a similar way to ``characteristic``'s is still supported.
- The names are held shorter and easy to both type and read.
- It is generally more opinionated towards typical uses.
  This ensures I'll not wake up in a year hating to use it.
- The generated ``__init__`` methods are faster because of certain features that have been left out intentionally.
  The generated code should be as fast as hand-written one.
