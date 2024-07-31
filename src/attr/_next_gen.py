# SPDX-License-Identifier: MIT

"""
These are keyword-only APIs that call `attr.s` and `attr.ib` with different
default values.
"""


from functools import partial

from . import setters
from ._funcs import asdict as _asdict
from ._funcs import astuple as _astuple
from ._make import (
    _DEFAULT_ON_SETATTR,
    NOTHING,
    _frozen_setattrs,
    attrib,
    attrs,
)
from .exceptions import UnannotatedAttributeError


def define(
    maybe_cls=None,
    *,
    these=None,
    repr=None,
    unsafe_hash=None,
    hash=None,
    init=None,
    slots=True,
    frozen=False,
    weakref_slot=True,
    str=False,
    auto_attribs=None,
    kw_only=False,
    cache_hash=False,
    auto_exc=True,
    eq=None,
    order=False,
    auto_detect=True,
    getstate_setstate=None,
    on_setattr=None,
    field_transformer=None,
    match_args=True,
):
    r"""
    A class decorator that adds :term:`dunder methods` according to the
    specified attributes using `attr.ib` or the *these* argument.

    Args:
        slots (bool):
            Create a :term:`slotted class <slotted classes>` that's more
            memory-efficient. Slotted classes are generally superior to the
            default dict classes, but have some gotchas you should know about,
            so we encourage you to read the :term:`glossary entry <slotted
            classes>`.

        auto_detect (bool):
            Instead of setting the *init*, *repr*, *eq*, and *hash* arguments
            explicitly, assume they are set to True **unless any** of the
            involved methods for one of the arguments is implemented in the
            *current* class (meaning, it is *not* inherited from some base
            class).

            So, for example by implementing ``__eq__`` on a class yourself,
            *attrs* will deduce ``eq=False`` and will create *neither*
            ``__eq__`` *nor* ``__ne__`` (but Python classes come with a
            sensible ``__ne__`` by default, so it *should* be enough to only
            implement ``__eq__`` in most cases).

            Passing True or False` to *init*, *repr*, *eq*, *cmp*, or *hash*
            overrides whatever *auto_detect* would determine.

        auto_exc (bool):
            If the class subclasses `BaseException` (which implicitly includes
            any subclass of any exception), the following happens to behave
            like a well-behaved Python exception class:

            - the values for *eq*, *order*, and *hash* are ignored and the
              instances compare and hash by the instance's ids [#]_ ,
            - all attributes that are either passed into ``__init__`` or have a
              default value are additionally available as a tuple in the
              ``args`` attribute,
            - the value of *str* is ignored leaving ``__str__`` to base
              classes.

            .. [#]
               Note that *attrs* will *not* remove existing implementations of
               ``__hash__`` or the equality methods. It just won't add own
               ones.

        on_setattr (~typing.Callable | list[~typing.Callable] | None | typing.Literal[attrs.setters.NO_OP]):
            A callable that is run whenever the user attempts to set an
            attribute (either by assignment like ``i.x = 42`` or by using
            `setattr` like ``setattr(i, "x", 42)``). It receives the same
            arguments as validators: the instance, the attribute that is being
            modified, and the new value.

            If no exception is raised, the attribute is set to the return value
            of the callable.

            If a list of callables is passed, they're automatically wrapped in
            an `attrs.setters.pipe`.

            If left None, the default behavior is to run converters and
            validators whenever an attribute is set.

        init (bool):
            Create a ``__init__`` method that initializes the *attrs*
            attributes. Leading underscores are stripped for the argument name,
            unless an alias is set on the attribute.

            .. seealso::
                `init` shows advanced ways to customize the generated
                ``__init__`` method, including executing code before and after.

        repr(bool):
            Create a ``__repr__`` method with a human readable representation
            of *attrs* attributes.

        str (bool):
            Create a ``__str__`` method that is identical to ``__repr__``. This
            is usually not necessary except for `Exception`\ s.

        eq (bool | None):
            If True or None (default), add ``__eq__`` and ``__ne__``
            methods that check two instances for equality.

            .. seealso::
                `comparison` describes how to customize the comparison behavior
                going as far comparing NumPy arrays.

        order (bool | None):
            If True, add ``__lt__``, ``__le__``, ``__gt__``, and ``__ge__``
            methods that behave like *eq* above and allow instances to be
            ordered.

            They compare the instances as if they were tuples of their *attrs*
            attributes if and only if the types of both classes are
            *identical*.

            If `None` mirror value of *eq*.

            .. seealso:: `comparison`

        cmp (bool | None):
            Setting *cmp* is equivalent to setting *eq* and *order* to the same
            value. Must not be mixed with *eq* or *order*.

        unsafe_hash (bool | None):
            If None (default), the ``__hash__`` method is generated according
            how *eq* and *frozen* are set.

            1. If *both* are True, *attrs* will generate a ``__hash__`` for
               you.
            2. If *eq* is True and *frozen* is False, ``__hash__`` will be set
               to None, marking it unhashable (which it is).
            3. If *eq* is False, ``__hash__`` will be left untouched meaning
               the ``__hash__`` method of the base class will be used. If the
               base class is `object`, this means it will fall back to
               id-based hashing.

            Although not recommended, you can decide for yourself and force
            *attrs* to create one (for example, if the class is immutable even
            though you didn't freeze it programmatically) by passing True or
            not.  Both of these cases are rather special and should be used
            carefully.

            .. seealso::

                - Our documentation on `hashing`,
                - Python's documentation on `object.__hash__`,
                - and the `GitHub issue that led to the default \ behavior
                  <https://github.com/python-attrs/attrs/issues/136>`_ for more
                  details.

        hash (bool | None):
            Alias for *unsafe_hash*. *unsafe_hash* takes precedence.

        cache_hash (bool):
            Ensure that the object's hash code is computed only once and stored
            on the object.  If this is set to True, hashing must be either
            explicitly or implicitly enabled for this class.  If the hash code
            is cached, avoid any reassignments of fields involved in hash code
            computation or mutations of the objects those fields point to after
            object creation.  If such changes occur, the behavior of the
            object's hash code is undefined.

        frozen (bool):
            Make instances immutable after initialization.  If someone attempts
            to modify a frozen instance, `attrs.exceptions.FrozenInstanceError`
            is raised.

            .. note::

                1. This is achieved by installing a custom ``__setattr__``
                   method on your class, so you can't implement your own.

                2. True immutability is impossible in Python.

                3. This *does* have a minor a runtime performance `impact
                   <how-frozen>` when initializing new instances.  In other
                   words: ``__init__`` is slightly slower with ``frozen=True``.

                4. If a class is frozen, you cannot modify ``self`` in
                   ``__attrs_post_init__`` or a self-written ``__init__``. You
                   can circumvent that limitation by using
                   ``object.__setattr__(self, "attribute_name", value)``.

                5. Subclasses of a frozen class are frozen too.

        kw_only (bool):
            Make all attributes keyword-only in the generated ``__init__`` (if
            *init* is False, this parameter is ignored).

        weakref_slot (bool):
            Make instances weak-referenceable.  This has no effect unless
            *slots* is True.

        field_transformer (~typing.Callable | None):
            A function that is called with the original class object and all
            fields right before *attrs* finalizes the class.  You can use this,
            for example, to automatically add converters or validators to
            fields based on their types.

            .. seealso:: `transform-fields`

        match_args (bool):
            If True (default), set ``__match_args__`` on the class to support
            :pep:`634` (*Structural Pattern Matching*). It is a tuple of all
            non-keyword-only ``__init__`` parameter names on Python 3.10 and
            later. Ignored on older Python versions.

        collect_by_mro (bool):
            If True, *attrs* collects attributes from base classes correctly
            according to the `method resolution order
            <https://docs.python.org/3/howto/mro.html>`_. If False, *attrs*
            will mimic the (wrong) behavior of `dataclasses` and :pep:`681`.

            See also `issue #428
            <https://github.com/python-attrs/attrs/issues/428>`_.

        getstate_setstate (bool | None):
            .. note::

                This is usually only interesting for slotted classes and you
                should probably just set *auto_detect* to True.

            If True, ``__getstate__`` and ``__setstate__`` are generated and
            attached to the class. This is necessary for slotted classes to be
            pickleable. If left None, it's True by default for slotted classes
            and False for dict classes.

            If *auto_detect* is True, and *getstate_setstate* is left None, and
            **either** ``__getstate__`` or ``__setstate__`` is detected
            directly on the class (meaning: not inherited), it is set to False
            (this is usually what you want).

        auto_attribs (bool | None):
            If True, look at type annotations to determine which attributes to
            use, like `dataclasses`. If False, it will only look for explicit
            `field` class attributes, like classic *attrs*.

            If left None, it will guess:

            1. If any attributes are annotated and no unannotated
               `attrs.field`\ s are found, it assumes *auto_attribs=True*.
            2. Otherwise it assumes *auto_attribs=False* and tries to collect
               `attrs.field`\ s.

            If *attrs* decides to look at type annotations, **all** fields
            **must** be annotated. If *attrs* encounters a field that is set to
            a `field` / `attr.ib` but lacks a type annotation, an
            `attrs.exceptions.UnannotatedAttributeError` is raised.  Use
            ``field_name: typing.Any = attr.ib(...)`` if you don't want to set
            a type.

            .. warning::

                For features that use the attribute name to create decorators
                (for example, :ref:`validators <validators>`), you still *must*
                assign `field` / `attr.ib` to them. Otherwise Python will
                either not find the name or try to use the default value to
                call, for example, ``validator`` on it.

            Attributes annotated as `typing.ClassVar`, and attributes that are
            neither annotated nor set to an `attr.ib` are **ignored**.

        these (dict[str, object]):
            A dictionary of name to the (private) return value of `field()`
            mappings. This is useful to avoid the definition of your attributes
            within the class body because you can't (for example, if you want
            to add ``__repr__`` methods to Django models) or don't want to.

            If *these* is not `None`, *attrs* will *not* search the class body
            for attributes and will *not* remove any attributes from it.

            The order is deduced from the order of the attributes inside
            *these*.

            Arguably, this is a rather obscure feature.

    .. versionadded:: 20.1.0
    .. versionchanged:: 21.3.0 Converters are also run ``on_setattr``.
    .. versionadded:: 22.2.0
       *unsafe_hash* as an alias for *hash* (for :pep:`681` compliance).
    .. versionchanged:: 24.1.0

       Instances are not compared as tuples of attributes anymore, but using a
       big ``and`` condition. This is faster and has more correct behavior for
       uncomparable values like `math.nan`.

    .. note::

        The main differences to the classic `attr.s` are:

        - Automatically detect whether or not *auto_attribs* should be `True`
          (c.f. *auto_attribs* parameter).
        - Converters and validators run when attributes are set by default --
          if *frozen* is `False`.
        - *slots=True*

          Usually, this has only upsides and few visible effects in everyday
          programming. But it *can* lead to some surprising behaviors, so
          please make sure to read :term:`slotted classes`.

        - *auto_exc=True*
        - *auto_detect=True*
        - *order=False*
        - Some options that were only relevant on Python 2 or were kept around
          for backwards-compatibility have been removed.

    """

    def do_it(cls, auto_attribs):
        return attrs(
            maybe_cls=cls,
            these=these,
            repr=repr,
            hash=hash,
            unsafe_hash=unsafe_hash,
            init=init,
            slots=slots,
            frozen=frozen,
            weakref_slot=weakref_slot,
            str=str,
            auto_attribs=auto_attribs,
            kw_only=kw_only,
            cache_hash=cache_hash,
            auto_exc=auto_exc,
            eq=eq,
            order=order,
            auto_detect=auto_detect,
            collect_by_mro=True,
            getstate_setstate=getstate_setstate,
            on_setattr=on_setattr,
            field_transformer=field_transformer,
            match_args=match_args,
        )

    def wrap(cls):
        """
        Making this a wrapper ensures this code runs during class creation.

        We also ensure that frozen-ness of classes is inherited.
        """
        nonlocal frozen, on_setattr

        had_on_setattr = on_setattr not in (None, setters.NO_OP)

        # By default, mutable classes convert & validate on setattr.
        if frozen is False and on_setattr is None:
            on_setattr = _DEFAULT_ON_SETATTR

        # However, if we subclass a frozen class, we inherit the immutability
        # and disable on_setattr.
        for base_cls in cls.__bases__:
            if base_cls.__setattr__ is _frozen_setattrs:
                if had_on_setattr:
                    msg = "Frozen classes can't use on_setattr (frozen-ness was inherited)."
                    raise ValueError(msg)

                on_setattr = setters.NO_OP
                break

        if auto_attribs is not None:
            return do_it(cls, auto_attribs)

        try:
            return do_it(cls, True)
        except UnannotatedAttributeError:
            return do_it(cls, False)

    # maybe_cls's type depends on the usage of the decorator.  It's a class
    # if it's used as `@attrs` but `None` if used as `@attrs()`.
    if maybe_cls is None:
        return wrap

    return wrap(maybe_cls)


mutable = define
frozen = partial(define, frozen=True, on_setattr=None)


def field(
    *,
    default=NOTHING,
    validator=None,
    repr=True,
    hash=None,
    init=True,
    metadata=None,
    type=None,
    converter=None,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=None,
    alias=None,
):
    """
    Identical to `attr.ib`, except keyword-only and with some arguments
    removed.

    .. versionadded:: 23.1.0
       The *type* parameter has been re-added; mostly for `attrs.make_class`.
       Please note that type checkers ignore this metadata.
    .. versionadded:: 20.1.0
    """
    return attrib(
        default=default,
        validator=validator,
        repr=repr,
        hash=hash,
        init=init,
        metadata=metadata,
        type=type,
        converter=converter,
        factory=factory,
        kw_only=kw_only,
        eq=eq,
        order=order,
        on_setattr=on_setattr,
        alias=alias,
    )


def asdict(inst, *, recurse=True, filter=None, value_serializer=None):
    """
    Same as `attr.asdict`, except that collections types are always retained
    and dict is always used as *dict_factory*.

    .. versionadded:: 21.3.0
    """
    return _asdict(
        inst=inst,
        recurse=recurse,
        filter=filter,
        value_serializer=value_serializer,
        retain_collection_types=True,
    )


def astuple(inst, *, recurse=True, filter=None):
    """
    Same as `attr.astuple`, except that collections types are always retained
    and `tuple` is always used as the *tuple_factory*.

    .. versionadded:: 21.3.0
    """
    return _astuple(
        inst=inst, recurse=recurse, filter=filter, retain_collection_types=True
    )
