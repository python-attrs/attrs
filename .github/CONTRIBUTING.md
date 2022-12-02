# How To Contribute

Thank you for considering contributing to *attrs*!
It's people like *you* who make it such a great tool for everyone.

This document intends to make contribution more accessible by codifying tribal knowledge and expectations.
Don't be afraid to open half-finished PRs, and ask questions if something is unclear!

Please note that this project is released with a Contributor [Code of Conduct](https://github.com/python-attrs/attrs/blob/main/.github/CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.
Please report any harm to [Hynek Schlawack] in any way you find appropriate.


## Support

In case you'd like to help out but don't want to deal with GitHub, there's a great opportunity:
help your fellow developers on [Stack Overflow](https://stackoverflow.com/questions/tagged/python-attrs)!

The official tag is `python-attrs` and helping out in support frees us up to improve *attrs* instead!


## Workflow

- No contribution is too small!
  Please submit as many fixes for typos and grammar bloopers as you can!
- Try to limit each pull request to *one* change only.
- Since we squash on merge, it's up to you how you handle updates to the `main` branch.
  Whether you prefer to rebase on `main` or merge `main` into your branch, do whatever is more comfortable for you.
- *Always* add tests and docs for your code.
  This is a hard rule; patches with missing tests or documentation won't be merged.
- Make sure your changes pass our [CI].
  You won't get any feedback until it's green unless you ask for it.
- For the CI to pass, the coverage must be 100%.
  If you have problems to test something, open anyway and ask for advice.
  In some situations, we may agree to add an `# pragma: no cover`.
- Once you've addressed review feedback, make sure to bump the pull request with a short note, so we know you're done.
- Don’t break backwards-compatibility.


## Local Development Environment

You can (and should) run our test suite using [*tox*].
However, you’ll probably want a more traditional environment as well.
We highly recommend to develop using the latest Python release because we try to take advantage of modern features whenever possible.

First create a [virtual environment](https://virtualenv.pypa.io/) so you don't break your system-wide Python installation.
It’s out of scope for this document to list all the ways to manage virtual environments in Python, but if you don’t already have a pet way, take some time to look at tools like [*direnv*](https://hynek.me/til/python-project-local-venvs/), [*virtualfish*](https://virtualfish.readthedocs.io/), and [*virtualenvwrapper*](https://virtualenvwrapper.readthedocs.io/).

Next, get an up-to-date checkout of the *attrs* repository:

```console
$ git clone git@github.com:python-attrs/attrs.git
```

or if you prefer to use *Git* via `https`:

```console
$ git clone https://github.com/python-attrs/attrs.git
```

Change into the newly created directory and **after activating your virtual environment** install an editable version of *attrs* along with its tests and docs requirements:

```console
$ cd attrs
$ python -m pip install --upgrade pip wheel setuptools  # PLEASE don't skip this step
$ python -m pip install -e '.[dev]'
```

At this point,

```console
$ python -m pytest
```

should work and pass.
You can *significantly* speed up the test suite by passing `-n auto` to *pytest* which activates [*pytest-xdist*](https://github.com/pytest-dev/pytest-xdist) and takes advantage of all your CPU cores.

Documentation should also build:

```console
$ cd docs
$ make html
```

The built documentation can then be found in `docs/_build/html/`.

---

To avoid committing code that violates our style guide, we strongly advise you to install [*pre-commit*] and its hooks:

```console
$ pre-commit install
```

This is not strictly necessary, because our [*tox*] file contains an environment that runs:

```console
$ pre-commit run --all-files
```

and our CI has integration with [pre-commit.ci](https://pre-commit.ci).
But it's way more comfortable to run it locally and *git* catching avoidable errors.


## Code

- Obey [PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/).
  We use the `"""`-on-separate-lines style for docstrings:

  ```python
  def func(x):
      """
      Do something.

      :param str x: A very important parameter.

      :rtype: str
      """
  ```
- If you add or change public APIs, tag the docstring using `..  versionadded:: 16.0.0 WHAT` or `..  versionchanged:: 16.2.0 WHAT`.
- We use [*isort*](https://github.com/PyCQA/isort) to sort our imports, and we use [*Black*](https://github.com/psf/black) with line length of 79 characters to format our code.
  As long as you run our full [*tox*] suite before committing, or install our [*pre-commit*] hooks (ideally you'll do both – see [*Local Development Environment*](#local-development-environment) above), you won't have to spend any time on formatting your code at all.
  If you don't, [CI] will catch it for you – but that seems like a waste of your time!


## Tests

- Write your asserts as `expected == actual` to line them up nicely:

  ```python
  x = f()

  assert 42 == x.some_attribute
  assert "foo" == x._a_private_attribute
  ```

- To run the test suite, all you need is a recent [*tox*].
  It will ensure the test suite runs with all dependencies against all Python versions just as it will in our [CI].
  If you lack some Python versions, you can can always limit the environments like `tox -e py38,py39`, or make it a non-failure using `tox --skip-missing-interpreters`.

  In that case you should look into [*asdf*](https://asdf-vm.com) or [*pyenv*](https://github.com/pyenv/pyenv), which make it very easy to install many different Python versions in parallel.
- Write [good test docstrings](https://jml.io/pages/test-docstrings.html).
- To ensure new features work well with the rest of the system, they should be also added to our [*Hypothesis*](https://hypothesis.readthedocs.io/) testing strategy, which can be found in `tests/strategies.py`.
- If you've changed or added public APIs, please update our type stubs (files ending in `.pyi`).


## Documentation

- Use [semantic newlines] in [*reStructuredText*] and [*Markdown*](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) files (files ending in `.rst` and `.md`):

  ```rst
  This is a sentence.
  This is another sentence.
  ```

- If you start a new section, add two blank lines before and one blank line after the header, except if two headers follow immediately after each other:

  ```rst
  Last line of previous section.


  Header of New Top Section
  -------------------------

  Header of New Section
  ^^^^^^^^^^^^^^^^^^^^^

  First line of new section.
  ```

- If you add a new feature, demonstrate its awesomeness on the [examples page](https://github.com/python-attrs/attrs/blob/main/docs/examples.rst)!


### Changelog

If your change is noteworthy, there needs to be a changelog entry so our users can learn about it!

To avoid merge conflicts, we use the [*Towncrier*](https://pypi.org/project/towncrier) package to manage our changelog.
*towncrier* uses independent *Markdown* files for each pull request – so called *news fragments* – instead of one monolithic changelog file.
On release, those news fragments are compiled into our [`CHANGELOG.md`](https://github.com/python-attrs/attrs/blob/main/CHANGELOG.md).

You don't need to install *Towncrier* yourself, you just have to abide by a few simple rules:

- For each pull request, add a new file into `changelog.d` with a filename adhering to the `pr#.(change|deprecation|breaking).md` schema:
  For example, `changelog.d/42.change.md` for a non-breaking change that is proposed in pull request #42.
- As with other docs, please use [semantic newlines] within news fragments.
- Wrap symbols like modules, functions, or classes into backticks so they are rendered in a `monospace font`.
- Wrap arguments into asterisks like in docstrings:
  `Added new argument *an_argument*.`
- If you mention functions or other callables, add parentheses at the end of their names:
  `attrs.func()` or `attrs.Class.method()`.
  This makes the changelog a lot more readable.
- Prefer simple past tense or constructions with "now".
  For example:

  + Added `attrs.validators.func()`.
  + `attrs.func()` now doesn't crash the Large Hadron Collider anymore when passed the *foobar* argument.
- If you want to reference multiple issues, copy the news fragment to another filename.
  *Towncrier* will merge all news fragments with identical contents into one entry with multiple links to the respective pull requests.

Example entries:

  ```md
  Added `attrs.validators.func()`.
  The feature really *is* awesome.
  ```

or:

  ```md
  `attrs.func()` now doesn't crash the Large Hadron Collider anymore when passed the *foobar* argument.
  The bug really *was* nasty.
  ```

---

``tox -e changelog`` will render the current changelog to the terminal if you have any doubts.


## Governance

*attrs* is maintained by [team of volunteers](https://github.com/python-attrs) that is always open to new members that share our vision of a fast, lean, and magic-free library that empowers programmers to write better code with less effort.
If you'd like to join, just get a pull request merged and ask to be added in the very same pull request!

**The simple rule is that everyone is welcome to review/merge pull requests of others but nobody is allowed to merge their own code.**

[Hynek Schlawack] acts reluctantly as the [BDFL](https://en.wikipedia.org/wiki/Benevolent_dictator_for_life) and has the final say over design decisions.


[CI]: https://github.com/python-attrs/attrs/actions?query=workflow%3ACI
[Hynek Schlawack]: https://hynek.me/about/
[*pre-commit*]: https://pre-commit.com/
[*tox*]: https://tox.wiki/
[semantic newlines]: https://rhodesmill.org/brandon/2012/one-sentence-per-line/
[*reStructuredText*]: https://www.sphinx-doc.org/en/stable/usage/restructuredtext/basics.html
