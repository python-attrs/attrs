# Summary

<!-- Please tell us what your pull request is about here. -->


# Pull Request Check List

<!--
This list is our brown M&M test:
Ignoring -- or even deleting -- leads to instant closing of this pull request.
The only exceptions are pure documentation fixes.

Please read our [contribution guide](https://github.com/python-attrs/attrs/blob/main/.github/CONTRIBUTING.md) at least once, it will save you unnecessary review cycles!

You may check boxes that don't apply to your pull request to indicate that there isn't anything left to do.
-->

- [ ] I acknowledge this project's [**AI policy**](https://github.com/python-attrs/attrs/blob/main/.github/AI_POLICY.md).
- [ ] This pull requests is [**not** from my `main` branch](https://hynek.me/articles/pull-requests-branch/).
  - Consider granting [push permissions to the PR branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/allowing-changes-to-a-pull-request-branch-created-from-a-fork), so maintainers can fix minor issues themselves without pestering you.
- [ ] There's **tests** for all new and changed code.
- [ ] Changes or additions to public APIs are reflected in our type stubs (files ending in ``.pyi``).
    - [ ] ...and used in the stub test file `typing-examples/baseline.py` or, if necessary, `typing-examples/mypy.py`.
    - [ ] If they've been added to `attr/__init__.pyi`, they've *also* been re-imported in `attrs/__init__.pyi`.
- [ ] The **documentation** has been updated.
    - [ ] New functions/classes have to be added to `docs/api.rst` by hand.
    - [ ] Changes to the signatures of `@attr.s()` and `@attrs.define()` have to be added by hand too.
    - [ ] Changed/added classes/methods/functions have appropriate `versionadded`, `versionchanged`, or `deprecated` [directives](http://www.sphinx-doc.org/en/stable/markup/para.html#directive-versionadded).
          The next version is the second number in the current release + 1.
          The first number represents the current year.
          So if the current version on PyPI is 26.2.0, the next version is gonna be 26.3.0.
          If the next version is the first in the new year, it'll be 27.1.0.
    - [ ] Documentation in `.rst` and `.md` files is written using [semantic newlines](https://rhodesmill.org/brandon/2012/one-sentence-per-line/).
- [ ] Changes have news fragments in [`changelog.d`](https://github.com/python-attrs/attrs/blob/main/changelog.d).

<!--
If you have *any* questions to *any* of the points above, just **submit and ask**!
Given the ongoing AI slop wave we need to be strict about policies, but we're happy to help out fellow humans.
-->
