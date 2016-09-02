"""
Commonly used conversion functions.
"""


from ._make import attr, attributes


@attributes(repr=False, slots=True)
class _ListOfConverter(object):
    type = attr()

    def __call__(self, src):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        return [self.type(**attrs) for attrs in src]

    def __repr__(self):
        return (
            "<list_of converter for type {type!r}>"
            .format(type=self.type))


def list_of(type):
    """
    Converter from an iterable of dicts of attributes to a list of a given type
    using keyword arguments to the constructor.

    :param type: The type in the resulting list
    :type type: type
    """
    return _ListOfConverter(type)


@attributes(repr=False, slots=True)
class _SetOfConverter(object):
    type = attr()

    def __call__(self, src):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        return set(self.type(**item) for item in src)

    def __repr__(self):
        return (
            "<set_of converter for type {type!r}>"
            .format(type=self.type))


def set_of(type):
    """
    Converter from an iterable of dicts of attributes to a set of a given type
    using keyword arguments to the constructor.

    :param type: The type in the resulting set
    :type type: type
    """
    return _SetOfConverter(type)


@attributes(repr=False, slots=True)
class _FrozensetOfConverter(object):
    type = attr()

    def __call__(self, src):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        return frozenset(self.type(**item) for item in src)

    def __repr__(self):
        return (
            "<frozenset_of converter for type {type!r}>"
            .format(type=self.type))


def frozenset_of(type):
    """
    Converter from an iterable of dicts of attributes to a set of a given type
    using keyword arguments to the constructor.

    :param type: The type in the resulting frozenset
    :type type: type
    """
    return _FrozensetOfConverter(type)


@attributes(repr=False, slots=True)
class _FromDictConverter(object):
    type = attr()

    def __call__(self, src):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        return self.type(**src)

    def __repr__(self):
        return (
            "<from_dict converter for type {type!r}>"
            .format(type=self.type))


def from_dict(type):
    """
    Converter from a dict of attributes to a given type.

    :param type: The type to convert to
    :type type: type
    """

    return _FromDictConverter(type)
