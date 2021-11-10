.. raw:: html

   <p align="center">
      <a href="https://www.attrs.org/">
         <img src="./docs/_static/attrs_logo.svg" width="35%" alt="attrs" />
      </a>
   </p>
   <p align="center">
      <a href="https://www.attrs.org/en/stable/?badge=stable">
          <img src="https://img.shields.io/badge/Docs-Read%20The%20Docs-black" alt="Documentation" />
      </a>
      <a href="https://github.com/python-attrs/attrs/blob/main/LICENSE">
         <img src="https://img.shields.io/badge/license-MIT-C06524" alt="License: MIT" />
      </a>
      <a href="https://pypi.org/project/attrs/">
         <img src="https://img.shields.io/pypi/v/attrs" />
      </a>
      <a href="https://pepy.tech/project/attrs">
         <img src="https://static.pepy.tech/personalized-badge/attrs?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads%20/%20Month" alt="Downloads per month" />
      </a>
   </p>

.. teaser-begin

``attrs`` is the Python package that will bring back the **joy** of **writing classes** by relieving you from the drudgery of implementing object protocols (aka `dunder <https://nedbatchelder.com/blog/200605/dunder.html>`_ methods).
`Trusted by NASA <https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/personalizing-your-profile#list-of-qualifying-repositories-for-mars-2020-helicopter-contributor-badge>`_ for Mars missions since 2020!

Its main goal is to help you to write **concise** and **correct** software without slowing down your code.

.. teaser-end

For that, it gives you a class decorator and a way to declaratively define the attributes on that class:

.. -code-begin-

.. code-block:: pycon

   >>> from typing import List
   >>> import attr

   >>> @attr.define
   ... class SomeClass:
   ...     a_number: int = 42
   ...     list_of_numbers: List[int] = attr.Factory(list)
   ...
   ...     def hard_math(self, another_number):
   ...         return self.a_number + sum(self.list_of_numbers) * another_number


   >>> sc = SomeClass(1, [1, 2, 3])
   >>> sc
   SomeClass(a_number=1, list_of_numbers=[1, 2, 3])

   >>> sc.hard_math(3)
   19
   >>> sc == SomeClass(1, [1, 2, 3])
   True
   >>> sc != SomeClass(2, [3, 2, 1])
   True

   >>> attr.asdict(sc)
   {'a_number': 1, 'list_of_numbers': [1, 2, 3]}

   >>> SomeClass()
   SomeClass(a_number=42, list_of_numbers=[])

   >>> C = attr.make_class("C", ["a", "b"])
   >>> C("foo", "bar")
   C(a='foo', b='bar')


After *declaring* your attributes ``attrs`` gives you:

- a concise and explicit overview of the class's attributes,
- a nice human-readable ``__repr__``,
- a complete set of comparison methods (equality and ordering),
- an initializer,
- and much more,

*without* writing dull boilerplate code again and again and *without* runtime performance penalties.

This gives you the power to use actual classes with actual types in your code instead of confusing ``tuple``\ s or `confusingly behaving <https://www.attrs.org/en/stable/why.html#namedtuples>`_ ``namedtuple``\ s.
Which in turn encourages you to write *small classes* that do `one thing well <https://www.destroyallsoftware.com/talks/boundaries>`_.
Never again violate the `single responsibility principle <https://en.wikipedia.org/wiki/Single_responsibility_principle>`_ just because implementing ``__init__`` et al is a painful drag.

----

In case you're wondering: this example uses ``attrs``'s `modern APIs <https://www.attrs.org/en/stable/api.html#next-generation-apis>`_ that have been introduced in version 20.1.0.
The old APIs (``@attr.s``, ``attr.ib``) will remain indefinitely.
`Type annotations <https://www.attrs.org/en/latest/types.html>`_ will also stay entirely **optional** forever.

.. -getting-help-

Getting Help
============

Please use the ``python-attrs`` tag on `Stack Overflow <https://stackoverflow.com/questions/tagged/python-attrs>`_ to get help.

Answering questions of your fellow developers is also a great way to help the project!


.. -project-information-

Project Information
===================

``attrs`` is released under the `MIT <https://choosealicense.com/licenses/mit/>`_ license,
its documentation lives at `Read the Docs <https://www.attrs.org/>`_,
the code on `GitHub <https://github.com/python-attrs/attrs>`_,
and the latest release on `PyPI <https://pypi.org/project/attrs/>`_.
It’s rigorously tested on Python 2.7, 3.5+, and PyPy.

We collect information on **third-party extensions** in our `wiki <https://github.com/python-attrs/attrs/wiki/Extensions-to-attrs>`_.
Feel free to browse and add your own!

If you'd like to contribute to ``attrs`` you're most welcome and we've written `a little guide <https://www.attrs.org/en/latest/contributing.html>`_ to get you started!


``attrs`` for Enterprise
------------------------

Available as part of the Tidelift Subscription.

The maintainers of ``attrs`` and thousands of other packages are working with Tidelift to deliver commercial support and maintenance for the open source packages you use to build your applications.
Save time, reduce risk, and improve code health, while paying the maintainers of the exact packages you use.
`Learn more. <https://tidelift.com/subscription/pkg/pypi-attrs?utm_source=pypi-attrs&utm_medium=referral&utm_campaign=enterprise&utm_term=repo>`_
