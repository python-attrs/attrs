import attr
import pytest
import unicodedata
from attr.exceptions import NotAnAttrsClassError

class TestAliasValidation:
    def test_invalid_identifier(self):
        """
        Invalid identifiers are rejected.
        """
        with pytest.raises(TypeError, match="Invalid initialization alias '1x'"):
            @attr.s
            class C:
                x = attr.ib(alias="1x")

    def test_keyword_alias(self):
        """
        Keywords are rejected.
        """
        with pytest.raises(TypeError, match="Invalid initialization alias 'class'"):
            @attr.s
            class C:
                x = attr.ib(alias="class")

    def test_self_shadowing(self):
        """
        'self' shadowing is rejected.
        """
        with pytest.raises(TypeError, match="shadows the 'self' parameter"):
            @attr.s
            class C:
                x = attr.ib(alias="self")

    def test_unicode_normalization_collision(self):
        """
        Aliases that collide after NFKC normalization are rejected.
        """
        omega = "\u03a9"
        ohm = "\u2126"
        assert omega != ohm
        assert unicodedata.normalize("NFKC", omega) == unicodedata.normalize("NFKC", ohm)

        with pytest.raises(TypeError, match="collides with another attribute's alias"):
            @attr.s
            class C:
                x = attr.ib(alias=omega)
                y = attr.ib(alias=ohm)

    def test_make_class_normalization_collision(self):
        """
        make_class also respects alias normalization collision checks.
        """
        omega = "\u03a9"
        ohm = "\u2126"
        
        with pytest.raises(TypeError, match="collides with another attribute's alias"):
            attr.make_class("C", {omega: attr.ib(), ohm: attr.ib()})

    def test_non_string_alias(self):
        """
        Non-string aliases are rejected.
        """
        with pytest.raises(TypeError, match="Invalid initialization alias 1"):
            @attr.s
            class C:
                x = attr.ib(alias=1)

    def test_valid_unicode_aliases(self):
        """
        Valid Unicode identifiers that don't collide are allowed.
        """
        @attr.s
        class C:
            π = attr.ib()
            α = attr.ib(alias="beta")
        
        inst = C(π=3.14, beta=1)
        assert inst.π == 3.14
        assert inst.α == 1

    def test_init_false_skipped(self):
        """
        Validation is skipped if init=False.
        """
        @attr.s
        class C:
            x = attr.ib(init=False, alias="not an identifier!")
        
        inst = C()
        inst.x = 42
        assert inst.x == 42
