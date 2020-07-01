import attr


class TestAttred(object):
    def test_on_function(self):
        @attr.ed(short_description="Full Name")
        def example_django_admin_function_full_name():
            first_name = "Attr"
            last_name = "Ed"
            return "{} {}".format(first_name, last_name)

        assert (
            "Full Name"
            == example_django_admin_function_full_name.short_description
        )

    def test_on_method(self):
        class Model:
            first_name = "Attr"
            last_name = "Ed"

            @attr.ed(short_description="Full Name")
            def get_full_name(self):
                return "{} {}".format(self.first_name, self.last_name)

        assert "Full Name" == Model().get_full_name.short_description

    def test_on_class_and_instance(self):
        @attr.ed(short_description="Full Name")
        class AttrEd:
            ...

        assert "Full Name" == AttrEd.short_description
        assert "Full Name" == AttrEd().short_description
