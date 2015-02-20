.. _examples:

Examples
========


Basics
------

The simplest possible usage would be:

.. doctest::

   >>> import attr
   >>> @attr.s
   ... class Empty(object):
   ...     pass
   >>> Empty()
   Empty()
   >>> Empty() == Empty()
   True
   >>> Empty() is Empty()
   False

So in other words: ``attrs`` useful even without actual attributes!

But you'll usually want some data on your classes, so let's add some:

.. doctest::

   >>> @attr.s
   ... class Coordinates(object):
   ...     x = attr.ib()
   ...     y = attr.ib()

These by default, all features are added, so you have immediately a fully functional data class with a nice ``repr`` string and comparison methods.

.. doctest::

   >>> c1 = Coordinates(1, 2)
   >>> c1
   Coordinates(x=1, y=2)
   >>> c2 = Coordinates(x=2, y=1)
   >>> c2
   Coordinates(x=2, y=1)
   >>> c1 == c2
   False

As shown, the generated ``__init__`` method allows both for positional and keyword arguments.

If playful naming turns you off, ``attrs`` comes with no-nonsense aliases:

.. doctest::

   >>> @attr.attributes
   ... class SeriousCoordinates(object):
   ...     x = attr.attr()
   ...     y = attr.attr()
   >>> SeriousCoordinates(1, 2)
   SeriousCoordinates(x=1, y=2)
   >>> attr.fields(Coordinates) == attr.fields(SeriousCoordinates)
   True

For private attributes, ``attrs`` will strip the leading underscores for keyword arguments:

.. doctest::

   >>> @attr.s
   ... class C(object):
   ...     _x = attr.ib()
   >>> C(x=1)
   C(_x=1)

An additional way (not unlike ``characteristic``) of defining attributes is supported too.
This is useful in times when you want to enhance classes that are not yours (nice ``__repr__`` for Django models anyone?):

.. doctest::

   >>> class SomethingFromSomeoneElse(object):
   ...     def __init__(self, x):
   ...         self.x = x
   >>> SomethingFromSomeoneElse = attr.s(these={"x": attr.ib()}, init=False)(SomethingFromSomeoneElse)
   >>> SomethingFromSomeoneElse(1)
   SomethingFromSomeoneElse(x=1)

Or if you want to use properties:

.. doctest::

   >>> @attr.s(these={"_x": attr.ib()})
   ... class ReadOnlyXSquared(object):
   ...    @property
   ...    def x(self):
   ...       return self._x ** 2
   >>> rox = ReadOnlyXSquared(x=5)
   >>> rox
   ReadOnlyXSquared(_x=5)
   >>> rox.x
   25
   >>> rox.x = 6
   Traceback (most recent call last):
      ...
   AttributeError: can't set attribute

`Sub-classing <https://www.youtube.com/watch?v=3MNVP9-hglc>`_ is bad for you, but ``attrs`` will still do what you'd hope for:

.. doctest::

   >>> @attr.s
   ... class A(object):
   ...     a = attr.ib()
   ...     def get_a(self):
   ...         return self.a
   >>> @attr.s
   ... class B(object):
   ...     b = attr.ib()
   >>> @attr.s
   ... class C(B, A):
   ...     c = attr.ib()
   >>> i = C(1, 2, 3)
   >>> i
   C(a=1, b=2, c=3)
   >>> i == C(1, 2, 3)
   True
   >>> i.get_a()
   1

The order of the attributes is defined by the `MRO <https://www.python.org/download/releases/2.3/mro/>`_.

In Python 3, classes defined within other classes are `detected <https://www.python.org/dev/peps/pep-3155/>`_ and reflected in the ``__repr__``.
In Python 2 though, it's impossible.
Therefore ``@attr.s`` comes with the ``repr_ns`` option to set it manually:

.. doctest::

   >>> @attr.s
   ... class C(object):
   ...     @attr.s(repr_ns="C")
   ...     class D(object):
   ...         pass
   >>> C.D()
   C.D()

``repr_ns`` works on both Python 2 and 3.
On Python 3 is overrides the implicit detection.


Converting to Dictionaries
--------------------------

When you have a class with data, it often is very convenient to transform that class into a :class:`dict` (for example if you want to serialize it to JSON):

.. doctest::

   >>> attr.asdict(Coordinates(x=1, y=2))
   {'y': 2, 'x': 1}

Some fields cannot or should not be transformed.
For that, :func:`attr.asdict` offers a callback that decides whether an attribute should be included:

.. doctest::

   >>> @attr.s
   ... class UserList(object):
   ...     users = attr.ib()
   >>> @attr.s
   ... class User(object):
   ...     email = attr.ib()
   ...     password = attr.ib()
   >>> attr.asdict(UserList([User("jane@doe.invalid", "s33kred"),
   ...                       User("joe@doe.invalid", "p4ssw0rd")]),
   ...             filter=lambda attr, value: attr.name != "password")
   {'users': [{'email': 'jane@doe.invalid'}, {'email': 'joe@doe.invalid'}]}

For the common case where you want to :func:`include <attr.filters.include>` or :func:`exclude <attr.filters.exclude>` certain types or attributes, ``attrs`` ships with a few helpers:

.. doctest::

   >>> @attr.s
   ... class User(object):
   ...     login = attr.ib()
   ...     password = attr.ib()
   ...     id = attr.ib()
   >>> attr.asdict(User("jane", "s33kred", 42), filter=attr.filters.exclude(User.password, int))
   {'login': 'jane'}
   >>> @attr.s
   ... class C(object):
   ...     x = attr.ib()
   ...     y = attr.ib()
   ...     z = attr.ib()
   >>> attr.asdict(C("foo", "2", 3), filter=attr.filters.include(int, C.x))
   {'x': 'foo', 'z': 3}


Defaults
--------

Sometimes you want to have default values for your initializer.
And sometimes you even want mutable objects as default values (ever used accidentally ``def f(arg=[])``?).
``attrs`` has you covered in both cases:

.. doctest::

   >>> import collections
   >>> @attr.s
   ... class Connection(object):
   ...     socket = attr.ib()
   ...     @classmethod
   ...     def connect(cl, db_string):
   ...        # connect somehow to db_string
   ...        return cl(socket=42)
   >>> @attr.s
   ... class ConnectionPool(object):
   ...     db_string = attr.ib()
   ...     pool = attr.ib(default=attr.Factory(collections.deque))
   ...     debug = attr.ib(default=False)
   ...     def get_connection(self):
   ...         try:
   ...             return self.pool.pop()
   ...         except IndexError:
   ...             if self.debug:
   ...                 print "New connection!"
   ...             return Connection.connect(self.db_string)
   ...     def free_connection(self, conn):
   ...         if self.debug:
   ...             print "Connection returned!"
   ...         self.pool.appendleft(conn)
   ...
   >>> cp = ConnectionPool("postgres://localhost")
   >>> cp
   ConnectionPool(db_string='postgres://localhost', pool=deque([]), debug=False)
   >>> conn = cp.get_connection()
   >>> conn
   Connection(socket=42)
   >>> cp.free_connection(conn)
   >>> cp
   ConnectionPool(db_string='postgres://localhost', pool=deque([Connection(socket=42)]), debug=False)

More information on why class methods for constructing objects are awesome can be found in this insightful `blog post <http://as.ynchrono.us/2014/12/asynchronous-object-initialization.html>`_.


Validators
----------

Although your initializers should be a dumb as possible, it can come handy to do some kind of validation on the arguments.
That's when :func:`attr.ib`\ ’s ``validator`` argument comes into play.
A validator is simply a callable that takes three arguments:

#. The *instance* that's being validated.
#. The *attribute* that it's validating
#. and finally the *value* that is passed for it.

If the value does not pass the validator's standards, it just raises an appropriate exception.
Since the validator runs *after* the instance is initialized, you can refer to other attributes while validating :

.. doctest::

   >>> def x_smaller_than_y(instance, attribute, value):
   ...     if value >= instance.y:
   ...         raise ValueError("'x' has to be smaller than 'y'!")
   >>> @attr.s
   ... class C(object):
   ...     x = attr.ib(validator=x_smaller_than_y)
   ...     y = attr.ib()
   >>> C(x=3, y=4)
   C(x=3, y=4)
   >>> C(x=4, y=3)
   Traceback (most recent call last):
      ...
   ValueError: 'x' has to be smaller than 'y'!

``attrs`` won't intercept your changes to those attributes but you can always call :func:`attr.validate` on any instance to verify, that it's still valid:

.. doctest::

   >>> i = C(4, 5)
   >>> i.x = 5  # works, no magic here
   >>> attr.validate(i)
   Traceback (most recent call last):
      ...
   ValueError: 'x' has to be smaller than 'y'!

``attrs`` ships with a bunch of validators, make sure to :ref:`check them out <api_validators>` before writing your own:

.. doctest::

   >>> @attr.s
   ... class C(object):
   ...     x = attr.ib(validator=attr.validators.instance_of(int))
   >>> C(42)
   C(x=42)
   >>> C("42")
   Traceback (most recent call last):
      ...
   TypeError: ("'x' must be <type 'int'> (got '42' that is a <type 'str'>).", Attribute(name='x', default=NOTHING, factory=NOTHING, validator=<instance_of validator for type <type 'int'>>), <type 'int'>, '42')

If you like `zope.interface <http://docs.zope.org/zope.interface/api.html#zope-interface-interface-specification>`_, ``attrs`` also comes with a :func:`attr.validators.provides` validator:

.. doctest::

   >>> import zope.interface
   >>> class IFoo(zope.interface.Interface):
   ...     def f():
   ...         """A function called f."""
   >>> @attr.s
   ... class C(object):
   ...     x = attr.ib(validator=attr.validators.provides(IFoo))
   >>> C(x=object())
   Traceback (most recent call last):
      ...
   TypeError: ("'x' must provide <InterfaceClass __builtin__.IFoo> which <object object at 0x10bafaaf0> doesn't.", Attribute(name='x', default=NOTHING, factory=NOTHING, validator=<provides validator for interface <InterfaceClass __builtin__.IFoo>>), <InterfaceClass __builtin__.IFoo>, <object object at 0x10bafaaf0>)
   >>> @zope.interface.implementer(IFoo)
   ... @attr.s
   ... class Foo(object):
   ...     def f(self):
   ...         print("hello, world")
   >>> C(Foo())
   C(x=Foo())

You can also disable them globally:

   >>> attr.set_run_validators(False)
   >>> C(42)
   C(x=42)
   >>> attr.set_run_validators(True)
   >>> C(42)
   Traceback (most recent call last):
      ...
   TypeError: ("'x' must provide <InterfaceClass __builtin__.IFoo> which 42 doesn't.", Attribute(name='x', default=NOTHING, validator=<provides validator for interface <InterfaceClass __builtin__.IFoo>>, repr=True, cmp=True, hash=True, init=True), <InterfaceClass __builtin__.IFoo>, 42)


Other Goodies
-------------

Do you like Rich Hickey?
I'm glad to report that Clojure's core feature is part of ``attrs``: `assoc <https://clojuredocs.org/clojure.core/assoc>`_!
I guess that means Clojure can be shut down now, sorry Rich!

.. doctest::

   >>> @attr.s
   ... class C(object):
   ...     x = attr.ib()
   ...     y = attr.ib()
   >>> i1 = C(1, 2)
   >>> i1
   C(x=1, y=2)
   >>> i2 = attr.assoc(i1, y=3)
   >>> i2
   C(x=1, y=3)
   >>> i1 == i2
   False

Sometimes you may want to create a class programmatically.
``attrs`` won't let you down:

.. doctest::

   >>> @attr.s
   ... class C1(object):
   ...     x = attr.ib()
   ...     y = attr.ib()
   >>> C2 = attr.make_class("C2", ["x", "y"])
   >>> attr.fields(C1) == attr.fields(C2)
   True

You can still have power over the attributes if you pass a dictionary of name: ``attr.ib`` mappings and can pass arguments to ``@attr.s``:

.. doctest::

   >>> C = attr.make_class("C", {"x": attr.ib(default=42),
   ...                           "y": attr.ib(default=attr.Factory(list))},
   ...                     repr=False)
   >>> i = C()
   >>> i  # no repr added!
   <attr._make.C object at ...>
   >>> i.x
   42
   >>> i.y
   []

Finally, you can exclude single attributes from certain methods:

.. doctest::

   >>> @attr.s
   ... class C(object):
   ...     user = attr.ib()
   ...     password = attr.ib(repr=False)
   >>> C("me", "s3kr3t")
   C(user='me')
