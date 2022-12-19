# SPDX-License-Identifier: MIT

import codecs
import os
import re

from setuptools import find_packages, setup


###############################################################################

NAME = "attrs"
PACKAGES = find_packages(where="src")
META_PATH = os.path.join("src", "attr", "__init__.py")
KEYWORDS = ["class", "attribute", "boilerplate", "dataclass"]
PROJECT_URLS = {
    "Documentation": "https://www.attrs.org/",
    "Changelog": "https://www.attrs.org/en/stable/changelog.html",
    "Bug Tracker": "https://github.com/python-attrs/attrs/issues",
    "Source Code": "https://github.com/python-attrs/attrs",
    "Funding": "https://github.com/sponsors/hynek",
    "Tidelift": "https://tidelift.com/subscription/pkg/pypi-attrs?"
    "utm_source=pypi-attrs&utm_medium=pypi",
    "Ko-fi": "https://ko-fi.com/the_hynek",
}
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = []
EXTRAS_REQUIRE = {
    "docs": [
        "furo",
        "sphinx",
        "myst-parser",
        "zope.interface",
        "sphinx-notfound-page",
        "sphinxcontrib-towncrier",
        "towncrier",
    ],
    "tests-no-zope": [
        # For regression test to ensure cloudpickle compat doesn't break.
        'cloudpickle; python_implementation == "CPython"',
        "hypothesis",
        "pympler",
        # 4.3.0 dropped last use of `convert`
        "pytest>=4.3.0",
        # psutil extra is needed for correct core count detection.
        "pytest-xdist[psutil]",
        # Since the mypy error messages keep changing, we have to keep updating
        # this pin.
        "mypy>=0.971,<0.990; python_implementation == 'CPython'",
        "pytest-mypy-plugins; python_implementation == 'CPython' and "
        "python_version<'3.11'",
    ],
    "tests": [
        "attrs[tests-no-zope]",
        "zope.interface",
    ],
    "cov": [
        "attrs[tests]",
        "coverage-enable-subprocess",
        # Ensure coverage is new enough for `source_pkgs`.
        "coverage[toml]>=5.3",
    ],
    "dev": ["attrs[tests,docs]"],
}
# Don't break Paul unnecessarily just yet. C.f. #685
EXTRAS_REQUIRE["tests_no_zope"] = EXTRAS_REQUIRE["tests-no-zope"]


###############################################################################

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        rf"^__{meta}__ = ['\"]([^'\"]*)['\"]", META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(f"Unable to find __{meta}__ string.")


VERSION = find_meta("version")
URL = find_meta("url")

# PyPI doesn't support the <picture> tag.
LOGO = """<p align="center">
  <a href="https://www.attrs.org/">
    <img src="https://raw.githubusercontent.com/python-attrs/attrs/main/docs/_static/attrs_logo.svg" width="35%" alt="attrs" />
  </a>
</p>
"""  # noqa

LONG = (
    LOGO
    + read("README.md").split("<!-- logo-end -->", 1)[1]
    + "\n\n## Changes in This Release\n"
    + read("CHANGELOG.md")
    .split("towncrier release notes start -->", 1)[1]
    .strip()
    .split("\n## ", 1)[0]
    .strip()
    .split("\n", 1)[1]
    + "\n\n---\n\n[Full changelog]"
    "(https://www.attrs.org/en/stable/changelog.html)\n"
)

if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=LONG,
        long_description_content_type="text/markdown",
        packages=PACKAGES,
        package_dir={"": "src"},
        python_requires=">=3.6",
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        include_package_data=True,
    )
