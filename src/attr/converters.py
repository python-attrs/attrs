"""
Commonly used conversion functions.
"""


from ._make import attr, attributes


@attributes(repr=False, slots=True)
class _CollectionConverter(object):
    """
    Generic iterable to collection converter
    """
    type = attr()
    collection = attr()
    name = attr()

    def __call__(self, src):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        return self.collection(self._generator(src))

    def _generator(self, src):
        """
        Convert from a dict to self.type if necessary
        """
        for item in src:
            if isinstance(item, self.type):
                yield item
            else:
                yield self.type(**item)

    def __repr__(self):
        return (
            "<{name} converter for type {type!r}>"
            .format(name=self.name, type=self.type))


def list_of(type):
    """
    Converter from an iterable of dicts of attributes to a list of a given type
    using keyword arguments to the constructor.

    :param type: The type in the resulting list
    :type type: type
    """
    return _CollectionConverter(type=type, collection=list, name="list_of")


def set_of(type):
    """
    Converter from an iterable of dicts of attributes to a set of a given type
    using keyword arguments to the constructor.

    :param type: The type in the resulting set
    :type type: type
    """
    return _CollectionConverter(type=type, collection=set, name="set_of")


def frozenset_of(type):
    """
    Converter from an iterable of dicts of attributes or instances of `type` to
    a set of a given type using keyword arguments to the constructor.

    :param type: The type in the resulting frozenset
    :type type: type

    """
    return _CollectionConverter(type=type, collection=frozenset,
                                name="frozenset_of")


@attributes(repr=False, slots=True)
class _FromDictConverter(object):
    type = attr()

    def __call__(self, src):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        if isinstance(src, self.type):
            return src
        else:
            return self.type(**src)

    def __repr__(self):
        return (
            "<from_dict converter for type {type!r}>"
            .format(type=self.type))


def from_dict(type):
    """
    Converter from a dict of attributes or an instance of `type` to `type`.

    :param type: The type to convert to
    :type type: type
    """

    return _FromDictConverter(type)
