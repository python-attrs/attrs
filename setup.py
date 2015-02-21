import codecs
import os
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), "rb", "utf-8") as f:
        return f.read()


def find_version(*file_paths):
    """
    Build a path from *file_paths* and search for a ``__version__``
    string inside.
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args or [] +
                            ["tests"])
        sys.exit(errno)


if __name__ == "__main__":
    setup(
        name="attrs",
        version=find_version("attr/__init__.py"),
        description="Attributes without boilerplate.",
        long_description=(read("README.rst") + "\n\n" +
                          read("AUTHORS.rst")),
        url="https://attrs.readthedocs.org/",
        license="MIT",
        author="Hynek Schlawack",
        author_email="hs@ox.cx",
        packages=find_packages(exclude=['tests*']),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        install_requires=[
        ],
        tests_require=[
            "pytest",
            "zope.interface",
        ],
        cmdclass={
            "test": PyTest,
        },
        zip_safe=False,
    )
