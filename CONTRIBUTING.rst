How To Contribute
=================

First off, thank you for considering contributing to ``attrs``!
It's people like *you* who make it is such a great tool for everyone.

Here are a few guidelines to get you started (but don't be afraid to open half-finished PRs and ask questions if something is unclear!):


Workflow
--------

- No contribution is too small!
  Please submit as many fixes for typos and grammar bloopers as you can!
- Try to limit each pull request to *one* change only.
- *Always* add tests and docs for your code.
  This is a hard rule; patches with missing tests or documentation can't be accepted.
- Make sure your changes pass our CI_.
  You won't get any feedback until it's green unless you ask for it.
- Once you've addressed review feedback, make sure to bump the pull request with a short note.
  Maintainers don’t receive notifications when you push new commits.
- Don’t break `backward compatibility`_.


Code
----

- Obey `PEP 8`_ and `PEP 257`_.
  We use the ``"""``\ -on-separate-lines style for docstrings:

  .. code-block:: python

     def func(x):
         """
         Does something.

         :param str x: A very important parameter.

         :rtype: str
         """
- If you add or change public APIs, tag the docstring using ``..  versionadded:: 16.0.0 WHAT`` or ``..  versionchanged:: 16.2.0 WHAT``.
- Prefer double quotes (``"``) over single quotes (``'``) unless the string contains double quotes itself.


Tests
-----

- Write your asserts as ``expected == actual`` to line them up nicely:

  .. code-block:: python

     x = f()

     assert 42 == x.some_attribute
     assert "foo" == x._a_private_attribute

- To run the test suite, all you need is a recent tox_.
  It will ensure the test suite runs with all dependencies against all Python versions just as it will on Travis CI.
  If you lack some Python versions, you can can always limit the environments like ``tox -e py27,py35`` (in that case you may want to look into pyenv_, which makes it very easy to install many different Python versions in parallel).
- Write `good test docstrings`_.
- To ensure new features work well with the rest of the system, they should be also added to our `Hypothesis`_ testing strategy which you find in ``tests/util.py``.


Documentation
-------------

- Use `semantic newlines`_ in reStructuredText_ files (files ending in ``.rst``):

  .. code-block:: rst

     This is a sentence.
     This is another sentence.

- If you add a new feature, demonstrate its awesomeness in the `examples page`_!
- If your change is noteworthy, add an entry to the changelog_.
  Use present tense, `semantic newlines`_, and add a link to your pull request:

  .. code-block:: rst

     - Add awesome new feature.
       The feature really *is* awesome.
       [`#1 <https://github.com/hynek/attrs/pull/1>`_]
     - Fix nasty bug.
       The bug really *was* nasty.
       [`#2 <https://github.com/hynek/attrs/pull/2>`_]

****

Again, this list is mainly to help you to get started by codifying tribal knowledge and expectations.
If something is unclear, feel free to ask for help!

Please note that this project is released with a Contributor `Code of Conduct`_.
By participating in this project you agree to abide by its terms.
Please report any harm to `Hynek Schlawack`_ in any way you find appropriate.

Thank you for considering contributing to ``attrs``!


.. _`Hynek Schlawack`: https://hynek.me/about/
.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/
.. _`PEP 257`: https://www.python.org/dev/peps/pep-0257/
.. _`good test docstrings`: https://jml.io/pages/test-docstrings.html
.. _`Code of Conduct`: https://github.com/hynek/attrs/blob/master/CODE_OF_CONDUCT.rst
.. _changelog: https://github.com/hynek/attrs/blob/master/CHANGELOG.rst
.. _`backward compatibility`: https://attrs.readthedocs.io/en/latest/backward-compatibility.html
.. _`tox`: https://testrun.org/tox/
.. _pyenv: https://github.com/yyuu/pyenv
.. _reStructuredText: http://sphinx-doc.org/rest.html
.. _semantic newlines: http://rhodesmill.org/brandon/2012/one-sentence-per-line/
.. _examples page: https://github.com/hynek/attrs/blob/master/docs/examples.rst
.. _Hypothesis: https://hypothesis.readthedocs.org
.. _CI: https://travis-ci.org/hynek/attrs/
