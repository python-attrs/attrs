# SPDX-License-Identifier: MIT

"""
Public initializer behavior when parameters share the metadata helper name.
"""

import inspect

import pytest

import attrs


@pytest.mark.parametrize("alias", ["payload", "attr_dict"])
@pytest.mark.parametrize("payload", [{}, {"version": "user data"}])
def test_default_metadata(alias, payload, slots, frozen):
    """
    An alias preserves its value while non-init defaults use field metadata.
    """

    @attrs.define(slots=slots, frozen=frozen)
    class C:
        attributes: dict = attrs.field(alias=alias, kw_only=True)
        version: int = attrs.field(init=False, default=1)
        items: list = attrs.field(init=False, factory=list)

    instance = C(**{alias: payload})
    evolved = attrs.evolve(instance, **{alias: {"changed": True}})
    parameter = inspect.signature(C).parameters[alias]

    assert payload is instance.attributes
    assert 1 == instance.version == evolved.version
    assert [] == instance.items == evolved.items
    assert instance.items is not evolved.items
    assert {"changed": True} == evolved.attributes
    assert inspect.Parameter.KEYWORD_ONLY == parameter.kind
    assert dict is parameter.annotation


def test_natural_name_and_inherited_default(slots, frozen):
    """
    Natural field names and inherited defaults use the same safe metadata.
    """

    @attrs.define(slots=slots, frozen=frozen)
    class Base:
        version: int = attrs.field(init=False, default=1)

    @attrs.define(slots=slots, frozen=frozen)
    class C(Base):
        attr_dict: dict

    instance = C({})
    evolved = attrs.evolve(instance, attr_dict={"version": None})

    assert {} == instance.attr_dict
    assert {"version": None} == evolved.attr_dict
    assert 1 == instance.version == evolved.version


@pytest.mark.parametrize("takes_self", [False, True])
@pytest.mark.parametrize(
    ("init", "default_kind"),
    [
        (False, "scalar"),
        (False, "factory"),
        (True, "required"),
        (True, "scalar"),
        (True, "factory"),
    ],
)
def test_converter_metadata(init, default_kind, takes_self, slots, frozen):
    """
    Converters and validators receive the real field across assignment paths.
    """
    seen = []

    def convert(value, *args):
        field = args[-1]
        assert "version" == field.name
        if takes_self:
            assert {"version": "user data"} == args[0].attributes
        seen.append(field)
        return int(value)

    options = {"init": init, "kw_only": True}
    if default_kind == "scalar":
        options["default"] = "1"
    elif default_kind == "factory":
        options["factory"] = lambda: "1"

    @attrs.define(slots=slots, frozen=frozen)
    class C:
        attributes: dict = attrs.field(alias="attr_dict")
        version: int = attrs.field(
            converter=attrs.Converter(
                convert, takes_self=takes_self, takes_field=True
            ),
            validator=attrs.validators.instance_of(int),
            **options,
        )

    kwargs = {"version": "2"} if default_kind == "required" else {}
    instance = C(attr_dict={"version": "user data"}, **kwargs)
    evolved = attrs.evolve(instance)

    assert (2 if default_kind == "required" else 1) == instance.version
    assert instance.version == evolved.version
    assert [attrs.fields(C).version] * 2 == seen

    if not frozen:
        instance.version = "3"

        assert 3 == instance.version
        assert attrs.fields(C).version is seen[-1]


@pytest.mark.parametrize(
    "alias",
    ["attr_dict_", "\uff41\uff54\uff54\uff52_\uff44\uff49\uff43\uff54_"],
)
def test_multiple_metadata_name_collisions(alias):
    """
    Successive helper candidates and normalized aliases remain valid inputs.
    """

    @attrs.define
    class C:
        first: dict = attrs.field(alias="attr_dict")
        second: dict = attrs.field(alias=alias)
        third: dict = attrs.field(alias="attr_dict__")
        version: int = attrs.field(init=False, default=1)

    instance = C({}, {"version": "second"}, {})

    assert {} == instance.first == instance.third
    assert {"version": "second"} == instance.second
    assert 1 == instance.version
    assert ["attr_dict", "attr_dict_", "attr_dict__"] == list(
        inspect.signature(C).parameters
    )


def test_inherited_slotted_converter():
    """
    A frozen dict subclass converts inherited slotted defaults with metadata.
    """

    @attrs.frozen
    class Base:
        version: int = attrs.field(
            init=False,
            default="1",
            converter=attrs.Converter(
                lambda value, field: int(value) + len(field.name),
                takes_field=True,
            ),
        )

    @attrs.frozen(slots=False)
    class C(Base):
        attributes: dict = attrs.field(alias="attr_dict")

    instance = C(attr_dict={})

    assert 8 == instance.version == attrs.evolve(instance).version
    assert {} == instance.attributes


def test_attrs_init_metadata():
    """
    Custom constructors can delegate aliased arguments to __attrs_init__.
    """

    @attrs.define
    class C:
        attributes: dict = attrs.field(alias="attr_dict")
        version: int = attrs.field(init=False, default=1)

        def __init__(self, attr_dict):
            self.__attrs_init__(attr_dict=attr_dict)

    instance = C({})

    assert {} == instance.attributes
    assert 1 == instance.version == attrs.evolve(instance).version
