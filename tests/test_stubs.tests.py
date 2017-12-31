--  ---------------------------
--  Basics
--  ---------------------------

[case test_no_type]
import attr

@attr.s
class C:
    a = attr.ib()
    b = attr.ib(init=False, metadata={'foo': 1})

c = C(1)
reveal_type(c.a)  # E: Revealed type is 'Any'
reveal_type(C.a)  # E: Revealed type is 'Any'
reveal_type(c.b)  # E: Revealed type is 'Any'
reveal_type(C.b)  # E: Revealed type is 'Any'

[case test_type_arg]
# cmd: mypy --strict-optional
import attr
from typing import List

@attr.s
class C(object):
    a = attr.ib(type=int)

c = C(1)
reveal_type(c.a)  # E: Revealed type is 'builtins.int*'
reveal_type(C.a)  # E: Revealed type is 'builtins.int*'

C("1")     # E: Argument 1 to "C" has incompatible type "str"; expected "int"
C(a="1")   # E: Argument 1 to "C" has incompatible type "str"; expected "int"
C(None)    # E: Argument 1 to "C" has incompatible type "None"; expected "int"
C(a=None)  # E: Argument 1 to "C" has incompatible type "None"; expected "int"
C(a=1)

a = attr.ib(type=List[int])
reveal_type(a)  # E: Revealed type is 'builtins.list*[builtins.int*]'


[case test_type_annotations]
# cmd: mypy --strict-optional
import attr
from typing import List

@attr.s
class C(object):
    a : int = attr.ib()

c = C(1)
reveal_type(c.a)  # E: Revealed type is 'builtins.int'
reveal_type(C.a)  # E: Revealed type is 'builtins.int'

C("1")     # E: Argument 1 to "C" has incompatible type "str"; expected "int"
C(a="1")   # E: Argument 1 to "C" has incompatible type "str"; expected "int"
C(None)    # E: Argument 1 to "C" has incompatible type "None"; expected "int"
C(a=None)  # E: Argument 1 to "C" has incompatible type "None"; expected "int"
C(a=1)

a: List[int] = attr.ib()
reveal_type(a)  # E: Revealed type is 'builtins.list[builtins.int]'


--  ---------------------------
--  Defaults
--  ---------------------------

[case test_defaults_no_type]
import attr

a = attr.ib(default=0)
reveal_type(a)  # E: Revealed type is 'builtins.int*'

b = attr.ib(0)
reveal_type(b)  # E: Revealed type is 'builtins.int*'


[case test_defaults_type_arg]
import attr

a = attr.ib(type=int)
reveal_type(a)  # E: Revealed type is 'builtins.int*'

b = attr.ib(default=0, type=int)
reveal_type(b)  # E: Revealed type is 'builtins.int*'

c = attr.ib(default='bad', type=int)
# FXIME: this is now str.  should be error in line above.
reveal_type(c)  # E: Revealed type is 'builtins.object*'


[case test_defaults_type_annotations]
import attr

a: int = attr.ib()
reveal_type(a)  # E: Revealed type is 'builtins.int'

b: int = attr.ib(default=0)
reveal_type(b)  # E: Revealed type is 'builtins.int'

c: int = attr.ib(default='bad')  # E: Incompatible types in assignment (expression has type "str", variable has type "int")

# type arg is ignored.  should be error?
d: int = attr.ib(default=0, type=str)


--  ---------------------------
--  Factory Defaults
--  ---------------------------

[case test_factory_defaults_type_arg]
import attr
from typing import List

a = attr.ib(default=attr.Factory(list))
reveal_type(a)  # E: Revealed type is 'builtins.list*[_T`1]'

b = attr.ib(default=attr.Factory(list), type=List[int])
# FIXME: should be List[int]
reveal_type(b)  # E: Revealed type is 'builtins.list*[_T`1]'

c = attr.ib(default=attr.Factory(list), type=int)
# FIXME: should be int, and error should be generated above
reveal_type(c)  # E: Revealed type is 'builtins.list*[_T`1]'

def int_factory() -> int:
    return 0

d = attr.ib(default=attr.Factory(int_factory), type=int)
reveal_type(d)  # E: Revealed type is 'builtins.int*'


[case test_factory_defaults_type_annotations]
import attr
from typing import List

a = attr.ib(default=attr.Factory(list))
reveal_type(a)  # E: Revealed type is 'builtins.list*[_T`1]'

b: List[int] = attr.ib(default=attr.Factory(list))
reveal_type(b)  # E: Revealed type is 'builtins.list[builtins.int]'

c: int = attr.ib(default=attr.Factory(list))  # E: Incompatible types in assignment (expression has type "List[_T]", variable has type "int")

def int_factory() -> int:
    return 0

d: int = attr.ib(default=attr.Factory(int_factory))
reveal_type(d)  # E: Revealed type is 'builtins.int'


--  ---------------------------
--  Validators
--  ---------------------------

[case test_validators]
import attr
from attr.validators import in_, and_, instance_of
import enum

class State(enum.Enum):
    ON = "on"
    OFF = "off"

a =  attr.ib(type=int, validator=in_([1, 2, 3]))
aa = attr.ib(validator=in_([1, 2, 3]))

# multiple:
b =   attr.ib(type=int, validator=[in_([1, 2, 3]), instance_of(int)])
bb =  attr.ib(type=int, validator=(in_([1, 2, 3]), instance_of(int)))
bbb = attr.ib(type=int, validator=and_(in_([1, 2, 3]), instance_of(int)))

e = attr.ib(type=int, validator=1)  # E: No overload variant matches argument types [Overload(def (x: Union[builtins.str, builtins.bytes, typing.SupportsInt] =) -> builtins.int, def (x: Union[builtins.str, builtins.bytes], base: builtins.int) -> builtins.int), builtins.int]

# mypy does not know how to get the contained type from an enum:
f = attr.ib(type=State, validator=in_(State))
ff = attr.ib(validator=in_(State))  # E: Need type annotation for variable


[case test_init_with_validators]
import attr
from attr.validators import instance_of

@attr.s
class C:
    x = attr.ib(validator=instance_of(int))

reveal_type(C.x)  # E: Revealed type is 'builtins.int*'

C(42)
C(x=42)
# NOTE: even though the type of C.x is known to be int, the following is not an error.
# The mypy plugin that generates __init__ runs at semantic analysis time, but type inference (which handles TypeVars happens later)
C("42")
C(None)


[case test_custom_validators_type_arg]
import attr

def validate_int(inst, at, val: int):
    pass

def validate_str(inst, at, val: str):
    pass

a = attr.ib(type=int, validator=validate_int)  # int
b = attr.ib(type=int, validator=validate_str)  # E: Argument 2 has incompatible type "Callable[[Any, Any, str], Any]"; expected "Union[Callable[[Any, Attribute[Any], int], Any], List[Callable[[Any, Attribute[Any], int], Any]], Tuple[Callable[[Any, Attribute[Any], int], Any], ...]]"

reveal_type(a) # E: Revealed type is 'builtins.int'


[case test_custom_validators_type_annotations]
import attr

def validate_int(inst, at, val: int):
    pass

def validate_str(inst, at, val: str):
    pass

a: int = attr.ib(validator=validate_int)
b: int = attr.ib(validator=validate_str)  # E: Incompatible types in assignment (expression has type "str", variable has type "int")

reveal_type(a) # E: Revealed type is 'builtins.int'

--  ---------------------------
--  Converters
--  ---------------------------

[case test_converters]
import attr

def str_to_int(s: str) -> int:
    return int(s)

@attr.s
class C:
    x: int = attr.ib(convert=str_to_int)

C(1)
# FIXME: this should not be an error
# C('1')

--  ---------------------------
--  Make
--  ---------------------------

[case test_make_from_dict]
import attr
C = attr.make_class("C", {
    "x": attr.ib(type=int),
    "y": attr.ib()
})


[case test_make_from_str]
import attr
C = attr.make_class("C", ["x", "y"])


[case test_astuple]
import attr
@attr.s
class C:
    a: int = attr.ib()

t1 = attr.astuple(C)
reveal_type(t1)  # E: Revealed type is 'builtins.tuple[Any]'


[case test_asdict]
import attr
@attr.s
class C:
    a: int = attr.ib()

t1 = attr.asdict(C)
reveal_type(t1)  # E: Revealed type is 'builtins.dict[builtins.str, Any]'
