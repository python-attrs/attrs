# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import hashlib
import linecache
import sys


def _attrs_to_tuple(obj, attrs):
    """
    Create a tuple of all values of *obj*'s *attrs*.
    """
    return tuple(getattr(obj, a.name) for a in attrs)


def _add_hash(cl, attrs=None):
    if attrs is None:
        attrs = cl.__attrs_attrs__

    def hash_(self):
        """
        Automatically created by attrs.
        """
        return hash(_attrs_to_tuple(self, attrs))

    cl.__hash__ = hash_
    return cl


def _add_cmp(cl, attrs=None):
    if attrs is None:
        attrs = cl.__attrs_attrs__

    def attrs_to_tuple(obj):
        """
        Save us some typing.
        """
        return _attrs_to_tuple(obj, attrs)

    def eq(self, other):
        """
        Automatically created by attrs.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) == attrs_to_tuple(other)
        else:
            return NotImplemented

    def ne(self, other):
        """
        Automatically created by attrs.
        """
        result = eq(self, other)
        if result is NotImplemented:
            return NotImplemented
        else:
            return not result

    def lt(self, other):
        """
        Automatically created by attrs.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) < attrs_to_tuple(other)
        else:
            return NotImplemented

    def le(self, other):
        """
        Automatically created by attrs.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) <= attrs_to_tuple(other)
        else:
            return NotImplemented

    def gt(self, other):
        """
        Automatically created by attrs.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) > attrs_to_tuple(other)
        else:
            return NotImplemented

    def ge(self, other):
        """
        Automatically created by attrs.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) >= attrs_to_tuple(other)
        else:
            return NotImplemented

    cl.__eq__ = eq
    cl.__ne__ = ne
    cl.__lt__ = lt
    cl.__le__ = le
    cl.__gt__ = gt
    cl.__ge__ = ge

    return cl


def _add_repr(cl, attrs=None):
    if attrs is None:
        attrs = cl.__attrs_attrs__

    def repr_(self):
        """
        Automatically created by attrs.
        """
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(a.name + "=" + repr(getattr(self, a.name))
                      for a in attrs)
        )
    cl.__repr__ = repr_
    return cl


# I'm sorry. :(
if sys.version_info[0] == 2:
    def exec_(code, locals_, globals_):
        exec("exec code in locals_, globals_")
else:  # pragma: no cover
    def exec_(code, locals_, globals_):
        exec(code, locals_, globals_)


class _Nothing(object):
    """
    Sentinel class to indicate the lack of a value when ``None`` is ambiguous.
    """
    def __repr__(self):
        return "NOTHING"


NOTHING = _Nothing()
"""
Sentinel to indicate the lack of a value when ``None`` is ambiguous.
"""


def _add_init(cl):
    attrs = cl.__attrs_attrs__

    # We cache the generated init methods for the same kinds of attributes.
    sha1 = hashlib.sha1()
    sha1.update(repr(attrs).encode("utf-8"))
    unique_filename = "<attrs generated init {0}>".format(
        sha1.hexdigest()
    )

    script = _attrs_to_script(attrs)
    locs = {}
    bytecode = compile(script, unique_filename, "exec")
    attr_dict = dict((a.name, a) for a in attrs)
    exec_(bytecode, {"NOTHING": NOTHING, "attr_dict": attr_dict}, locs)
    init = locs["__init__"]

    # In order of debuggers like PDB being able to step through the code,
    # we add a fake linecache entry.
    linecache.cache[unique_filename] = (
        len(script),
        None,
        script.splitlines(True),
        unique_filename
    )
    cl.__init__ = init
    return cl


def _attrs_to_script(attrs):
    """
    Return a valid Python script of an initializer for *attrs*.
    """
    lines = []
    args = []
    for a in attrs:
        if a.validator is not None:
            lines.append("attr_dict['{name}'].validator({name})"
                         .format(name=a.name))
        if a.default_value is not NOTHING:
            args.append("{name}={default!r}".format(name=a.name,
                                                    default=a.default_value))
            lines.append("self.{name} = {name}".format(name=a.name))
        elif a.default_factory is not NOTHING:
            args.append("{name}=NOTHING".format(name=a.name))
            lines.extend("""\
if {name} is not NOTHING:
    self.{name} = {name}
else:
    self.{name} = attr_dict["{name}"].default_factory()"""
                         .format(name=a.name)
                         .split("\n"))
        else:
            args.append(a.name)
            lines.append("self.{name} = {name}".format(name=a.name))

    return """\
def __init__(self, {args}):
    '''
    Attribute initializer automatically created by attrs.
    '''
    {setters}
""".format(
        args=", ".join(args),
        setters="\n    ".join(lines),
    )
