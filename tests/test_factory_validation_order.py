import pytest

from attrs import define, field, validators


def test_default_factory_runs_after_required_validation():
    def make_b():
        return 10

    @define
    class Item:
        a: int = field(validator=validators.gt(0))
        b: int = field(
            default=None, factory=make_b, validator=validators.gt(0)
        )

    obj = Item(5)
    assert obj.b == 10


def test_cross_field_validator_sees_final_defaults():
    def cross_validate(instance, attribute, value):
        # b must always be greater than a
        if instance.b <= instance.a:
            raise ValueError("b must be greater than a")

    @define
    class Item:
        a: int = field()
        b: int = field(
            default=None, factory=lambda: 5, validator=cross_validate
        )

    with pytest.raises(ValueError):
        Item(5)

    # When user provides b manually, it should succeed
    assert Item(5, 10).b == 10


def test_missing_required_still_errors():
    @define
    class Thing:
        a: int = field()
        b: int = field(default=None, factory=lambda: 3)

    with pytest.raises(TypeError):
        Thing()


def test_independent_fields_unchanged():
    @define
    class Simple:
        x: int = field(validator=validators.gt(0))
        y: str = field(default="hi")

    obj = Simple(10)
    assert obj.y == "hi"
