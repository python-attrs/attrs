# SPDX-License-Identifier: MIT

"""
Initializer metadata preserves module types used by string annotations.
"""

from __future__ import annotations

import inspect
import typing

import pytest

import attrs


class attr_dict_:
    pass


class attr_dict__:
    pass


class attr_dict___:
    pass


@pytest.mark.parametrize(
    "alias",
    [
        "payload",
        "attr_dict",
        "\uff41\uff54\uff54\uff52_\uff44\uff49\uff43\uff54",
    ],
)
@pytest.mark.parametrize("with_default", [False, True])
def test_module_annotation_names(alias, with_default, slots, frozen):
    """
    Consecutive module names and normalized aliases preserve type identities.
    """

    @attrs.define(slots=slots, frozen=frozen)
    class Request:
        payload: attr_dict_ = attrs.field(alias=alias)
        second: attr_dict__ = attrs.field(alias="attr_dict_")
        third: attr_dict___

    if with_default:

        @attrs.define(slots=slots, frozen=frozen)
        class RequestWithDefault(Request):
            version: int = attrs.field(init=False, default=1)

        Request = RequestWithDefault

    value, second, third = attr_dict_(), attr_dict__(), attr_dict___()
    instance = Request(value, second, third)
    class_hints = typing.get_type_hints(Request)
    init_hints = typing.get_type_hints(Request.__init__)
    parameters = inspect.signature(Request).parameters

    assert value is instance.payload
    assert second is instance.second
    assert third is instance.third
    assert attr_dict_ is class_hints["payload"] is init_hints[alias]
    assert attr_dict__ is class_hints["second"] is init_hints["attr_dict_"]
    assert attr_dict___ is class_hints["third"] is init_hints["third"]
    assert [
        "payload" if alias == "payload" else "attr_dict",
        "attr_dict_",
        "third",
    ] == list(parameters)
    if alias.isascii():
        evolved = attrs.evolve(instance)

        assert value is evolved.payload
        assert second is evolved.second
        assert third is evolved.third
    if with_default:
        assert 1 == instance.version


def test_single_module_annotation_name(slots, frozen):
    """
    A renamed metadata helper preserves a previously resolvable module type.
    """

    @attrs.define(slots=slots, frozen=frozen)
    class Request:
        payload: attr_dict_ = attrs.field(alias="attr_dict")

    value = attr_dict_()
    instance = Request(attr_dict=value)

    assert value is instance.payload is attrs.evolve(instance).payload
    assert attr_dict_ is typing.get_type_hints(Request)["payload"]
    assert attr_dict_ is typing.get_type_hints(Request.__init__)["attr_dict"]
