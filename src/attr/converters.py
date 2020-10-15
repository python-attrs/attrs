"""
Commonly useful converters.
"""

from __future__ import absolute_import, division, print_function

from datetime import datetime

from ._make import NOTHING, Factory, pipe


__all__ = [
    "default_if_none",
    "optional",
    "pipe",
    "to_attrs",
    "to_dt",
    "to_iterable",
    "to_mapping",
    "to_tuple",
    "to_union",
]


NoneType = type(None)


def optional(converter):
    """
    A converter that allows an attribute to be optional. An optional attribute
    is one which can be set to ``None``.

    :param callable converter: the converter that is used for non-``None``
        values.

    .. versionadded:: 17.1.0
    """

    def optional_converter(val):
        if val is None:
            return None
        return converter(val)

    return optional_converter


def default_if_none(default=NOTHING, factory=None):
    """
    A converter that allows to replace ``None`` values by *default* or the
    result of *factory*.

    :param default: Value to be used if ``None`` is passed. Passing an instance
       of `attr.Factory` is supported, however the ``takes_self`` option
       is *not*.
    :param callable factory: A callable that takes not parameters whose result
       is used if ``None`` is passed.

    :raises TypeError: If **neither** *default* or *factory* is passed.
    :raises TypeError: If **both** *default* and *factory* are passed.
    :raises ValueError: If an instance of `attr.Factory` is passed with
       ``takes_self=True``.

    .. versionadded:: 18.2.0
    """
    if default is NOTHING and factory is None:
        raise TypeError("Must pass either `default` or `factory`.")

    if default is not NOTHING and factory is not None:
        raise TypeError(
            "Must pass either `default` or `factory` but not both."
        )

    if factory is not None:
        default = Factory(factory)

    if isinstance(default, Factory):
        if default.takes_self:
            raise ValueError(
                "`takes_self` is not supported by default_if_none."
            )

        def default_if_none_converter(val):
            if val is not None:
                return val

            return default.factory()

    else:

        def default_if_none_converter(val):
            if val is not None:
                return val

            return default

    return default_if_none_converter


def to_attrs(cls):
    """
    A converter that creates an instance of *cls* from a dict but leaves
    instances of that class as they are.

    Classes can define a ``from_dict()`` classmethod which will be called
    instead of the their `__init__()`.  This can be useful if you want to
    create different sub classes of *cls* depending on the data (e.g.,
    a ``Cat`` or a ``Dog`` inheriting ``Animal``).

    :param type cls: The class to convert data to.
    :returns: The converter function for *cls*.
    :rtype: callable

    .. versionadded:: 20.3.0

    """
    type_ = cls.from_dict if hasattr(cls, "from_dict") else cls

    def convert(val):
        if not isinstance(val, (cls, dict)):
            raise TypeError(
                f'Invalid type "{type(val).__name__}"; expected '
                f'"{cls.__name__}" or "dict".'
            )
        return type_(**val) if isinstance(val, dict) else val

    n = cls.__name__
    convert.__doc__ = f"""
        Convert *data* to an intance of {n} if it is not already an instance
        of it.

        :param Union[dict, {n}] data: The input data
        :returns: The converted data
        :rtype: {n}
        :raises TypeError: if *data* is neither a dict nor an instance of {n}.
        """

    return convert


def to_dt(val):
    """
    Convert an ISO formatted string to :class:`datetime.datetime`.  Leave the
    input untouched if it is already a datetime.

    See: :func:`datetime.datetime.fromisoformat`

    :param Union[str, datetime.datetime] data: The input data
    :returns: A parsed datetime object
    :rtype: datetime.datetime
    :raises TypeError: If *val* is neither a str nor a datetime.

    .. versionadded:: 20.3.0
    """
    if not isinstance(val, (datetime, str)):
        raise TypeError(
            f'Invalid type "{type(val).__name__}"; expected "datetime" or '
            f'"str".'
        )
    return datetime.fromisoformat(val) if isinstance(val, str) else val


def to_iterable(cls, converter):
    """
    A converter that creates a *cls* iterable (e.g., ``list``) and calls
    *converter* for each element.

    :param Type[Iterable] cls: The type of the iterable to create
    :param callable converter: The converter to apply to all items of the
        input data.
    :returns: The converter function
    :rtype: callable
    """

    def convert(val):
        return cls(converter(d) for d in val)

    return convert


def to_tuple(cls, converters):
    """
    A converter that creates a struct-like tuple (or namedtuple or similar)
    and converts each item via the corresponding converter from *converters*

    The input value must have exactly as many elements as there are converters.

    :param Type[Tuple] cls: The type of the tuple to create
    :param List[callable] converters: The respective converters for each tuple
        item.
    :returns: The converter function
    :rtype: callable
    """

    def convert(val):
        if len(val) != len(converters):
            raise TypeError(
                "Value must have {} items but has: {}".format(
                    len(converters), len(val)
                )
            )
        return cls(c(v) for c, v in zip(converters, val))

    return convert


def to_mapping(cls, key_converter, val_converter):
    """
    A converter that creates a mapping and converts all keys and values using
    the respective converters.

    :param Type[Mapping] cls: The mapping type to create (e.g., ``dict``).
    :param callable key_converter: The converter function to apply to all keys.
    :param callable val_converter: The converter function to apply to all
        values.
    :returns: The converter function
    :rtype: callable
    """

    def convert(val):
        return cls(
            (key_converter(k), val_converter(v)) for k, v in val.items()
        )

    return convert


def to_union(converters):
    """
    A converter that applies a number of converters to the input value and
    returns the result of the first converter that does not raise a
    :exc:`TypeError` or :exc:`ValueError`.

    If the input value already has one of the required types, it will be
    returned unchanged.

    :param List[callable] converters: A list of converters to try on the input.
    :returns: The converter function
    :rtype: callable

    """

    def convert(val):
        if type(val) in converters:
            # Preserve val as-is if it already has a matching type.
            # Otherwise float(3.2) would be converted to int
            # if the converters are [int, float].
            return val
        for converter in converters:
            try:
                return converter(val)
            except (TypeError, ValueError):
                pass
        raise ValueError(
            "Failed to convert value to any Union type: {}".format(val)
        )

    return convert
