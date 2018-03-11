# :---------------------------
# :Basics
# :---------------------------

# :Note: the attrs plugin for mypy only affects calls to attr.ib if they are
# :within a class definition, so we include a class in each test.


# [case test_no_type]
# :------------------
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


# [case test_type_arg]
# :-------------------
# cmd: mypy --strict-optional
import attr
from typing import List, Any

@attr.s
class C:
    a = attr.ib(type=int)

c = C(1)
reveal_type(c.a)  # E: Revealed type is 'builtins.int'
reveal_type(C.a)  # E: Revealed type is 'builtins.int'

C("1")     # E: Argument 1 to "C" has incompatible type "str"; expected "int"
C(a="1")   # E: Argument "a" to "C" has incompatible type "str"; expected "int"
C(None)    # E: Argument 1 to "C" has incompatible type "None"; expected "int"
C(a=None)  # E: Argument "a" to "C" has incompatible type "None"; expected "int"
C(a=1)

@attr.s
class D:
    a = attr.ib(type=List[int])
    reveal_type(a)  # E: Revealed type is 'builtins.list[builtins.int]'

@attr.s
class E:
    a = attr.ib(type='List[int]')
    reveal_type(a)  # E: Revealed type is 'builtins.list[builtins.int]'

@attr.s
class F:
    a = attr.ib(type=Any)
    reveal_type(a)  # E: Revealed type is 'Any'


# [case test_type_annotations]
# :---------------------------
# cmd: mypy --strict-optional
import attr
from typing import List, Any

@attr.s
class C:
    a: int = attr.ib()

c = C(1)
reveal_type(c.a)  # E: Revealed type is 'builtins.int'
reveal_type(C.a)  # E: Revealed type is 'builtins.int'

C("1")     # E: Argument 1 to "C" has incompatible type "str"; expected "int"
C(a="1")   # E: Argument "a" to "C" has incompatible type "str"; expected "int"
C(None)    # E: Argument 1 to "C" has incompatible type "None"; expected "int"
C(a=None)  # E: Argument "a" to "C" has incompatible type "None"; expected "int"
C(a=1)

@attr.s
class D:
    a: List[int] = attr.ib()
    reveal_type(a)  # E: Revealed type is 'builtins.list[builtins.int]'

@attr.s
class E:
    a: 'List[int]' = attr.ib()
    reveal_type(a)  # E: Revealed type is 'builtins.list[builtins.int]'

@attr.s
class F:
    a: Any = attr.ib()
    reveal_type(a)  # E: Revealed type is 'Any'


# [case test_inheritance]
# :----------------------
import attr

@attr.s
class A:
    x: int = attr.ib()

@attr.s
class B(A):
    y: str = attr.ib()

B(x=1, y='foo')
B(x=1, y=2)  # E: Argument "y" to "B" has incompatible type "int"; expected "str"


# [case test_multiple_inheritance]
# :----------------------
import attr

@attr.s
class A:
    x: int = attr.ib()

@attr.s
class B:
    y: str = attr.ib()

@attr.s
class C(B, A):
    z: float = attr.ib()

C(x=1, y='foo', z=1.1)
C(x=1, y=2, z=1.1)  # E: Argument "y" to "C" has incompatible type "int"; expected "str"


# [case test_dunders]
# :------------------
import attr

@attr.s
class A:
    x: int = attr.ib()

@attr.s
class B(A):
    y: str = attr.ib()

class C:
    pass

# same class
B(x=1, y='foo') == B(x=1, y='foo')
# child class
B(x=1, y='foo') == A(x=1)
# parent class
A(x=1) == B(x=1, y='foo')
# not attrs class
A(x=1) == C()

# same class
B(x=1, y='foo') > B(x=1, y='foo')
# child class
B(x=1, y='foo') > A(x=1)
# parent class
A(x=1) > B(x=1, y='foo')
# not attrs class
A(x=1) > C()  # E: Unsupported operand types for > ("A" and "C")


# :---------------------------
# :Defaults
# :---------------------------

# [case test_defaults_no_type]
# :----------------------------
import attr

@attr.s
class C:
    a = attr.ib(default=0)
    reveal_type(a)  # E: Revealed type is 'builtins.int*'

    b = attr.ib(0)
    reveal_type(b)  # E: Revealed type is 'builtins.int*'


# [case test_defaults_type_arg]
# :----------------------------
import attr

@attr.s
class C:
    a = attr.ib(type=int)
    reveal_type(a)  # E: Revealed type is 'builtins.int'

    b = attr.ib(default=0, type=int)
    reveal_type(b)  # E: Revealed type is 'builtins.int'

    c = attr.ib(default='bad', type=int)  # E: Incompatible types in assignment (expression has type "object", variable has type "int")


# [case test_defaults_type_annotations]
# :------------------------------------
import attr

@attr.s
class C:
    a: int = attr.ib()
    reveal_type(a)  # E: Revealed type is 'builtins.int'

    b: int = attr.ib(default=0)
    reveal_type(b)  # E: Revealed type is 'builtins.int'

    c: int = attr.ib(default='bad')  # E: Incompatible types in assignment (expression has type "str", variable has type "int")

    d: int = attr.ib(default=0, type=str)  # E: Incompatible types in assignment (expression has type "object", variable has type "int")


# :---------------------------
# :Factory Defaults
# :---------------------------

# [case test_factory_defaults_type_arg]
# :------------------------------------
import attr
from typing import List

def int_factory() -> int:
    return 0

@attr.s
class C:
    a = attr.ib(default=attr.Factory(list))
    reveal_type(a)  # E: Revealed type is 'builtins.list*[_T`1]'

    b = attr.ib(default=attr.Factory(list), type=List[int])
    reveal_type(b)  # E: Revealed type is 'builtins.list[builtins.int]'

    c = attr.ib(default=attr.Factory(list), type=int)  # E: Incompatible types in assignment (expression has type "object", variable has type "int")

    d = attr.ib(default=attr.Factory(int_factory), type=int)
    reveal_type(d)  # E: Revealed type is 'builtins.int'


# [case test_factory_defaults_type_annotations]
# :--------------------------------------------
import attr
from typing import List


def int_factory() -> int:
    return 0

@attr.s
class C:
    a = attr.ib(default=attr.Factory(list))
    reveal_type(a)  # E: Revealed type is 'builtins.list*[_T`1]'

    b: List[int] = attr.ib(default=attr.Factory(list))
    reveal_type(b)  # E: Revealed type is 'builtins.list[builtins.int]'

    c: int = attr.ib(default=attr.Factory(list))  # E: Incompatible types in assignment (expression has type "List[_T]", variable has type "int")

    d: int = attr.ib(default=attr.Factory(int_factory))
    reveal_type(d)  # E: Revealed type is 'builtins.int'


# :---------------------------
# :Validators
# :---------------------------

# [case test_validators]
# :---------------------
import attr
from attr.validators import in_, and_, instance_of
import enum

class State(enum.Enum):
    ON = "on"
    OFF = "off"

@attr.s
class C:
    a =  attr.ib(type=int, validator=in_([1, 2, 3]))
    aa = attr.ib(validator=in_([1, 2, 3]))

    # multiple:
    b =   attr.ib(type=int, validator=[in_([1, 2, 3]), instance_of(int)])
    bb =  attr.ib(type=int, validator=(in_([1, 2, 3]), instance_of(int)))
    bbb = attr.ib(type=int, validator=and_(in_([1, 2, 3]), instance_of(int)))

    e = attr.ib(type=int, validator=1)  # E: No overload variant of "ib" matches argument types [Overload(def (x: Union[builtins.str, builtins.bytes, typing.SupportsInt] =) -> builtins.int, def (x: Union[builtins.str, builtins.bytes], base: builtins.int) -> builtins.int), builtins.int]

    # mypy does not know how to get the contained type from an enum:
    f = attr.ib(type=State, validator=in_(State))
    ff = attr.ib(validator=in_(State))  # E: Need type annotation for 'ff'


# [case test_init_with_validators]
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


# [case test_custom_validators_type_arg]
# :-------------------------------------
import attr

def validate_int(inst, at, val: int):
    pass

def validate_str(inst, at, val: str):
    pass

@attr.s
class C:
    a = attr.ib(type=int, validator=validate_int)
    reveal_type(a)  # E: Revealed type is 'builtins.int'

    b = attr.ib(type=int, validator=[validate_int])
    reveal_type(b)  # E: Revealed type is 'builtins.int'

    c = attr.ib(type=int, validator=validate_str)  # E: Argument "validator" to "ib" has incompatible type "Callable[[Any, Any, str], Any]"; expected "Union[Callable[[Any, Attribute[Any], int], Any], Sequence[Callable[[Any, Attribute[Any], int], Any]]]"


# [case test_custom_validators_type_annotations]
# :---------------------------------------------
import attr

def validate_int(inst, at, val: int):
    pass

def validate_str(inst, at, val: str):
    pass

@attr.s
class C:
    a: int = attr.ib(validator=validate_int)
    reveal_type(a)  # E: Revealed type is 'builtins.int'

    b: int = attr.ib(validator=[validate_int])
    reveal_type(b)  # E: Revealed type is 'builtins.int'

    c: int = attr.ib(validator=validate_str)  # E: Incompatible types in assignment (expression has type "str", variable has type "int")


# :---------------------------
# :Converters
# :---------------------------

# [case test_converters]
# :---------------------
import attr
from typing import Union

def str_to_int(s: Union[str, int]) -> int:
    return int(s)

@attr.s
class C:
    a = attr.ib(converter=str_to_int)
    reveal_type(a)  # E: Revealed type is 'builtins.int*'

    b: str = attr.ib(converter=str_to_int)  # E: Incompatible types in assignment (expression has type "int", variable has type "str")


# [case test_converter_init]
# :-------------------------
import attr

def str_to_int(s: str) -> int:
    return int(s)

@attr.s
class C:
    x: int = attr.ib(converter=str_to_int)

C('1')
C(1)  # E: Argument 1 to "C" has incompatible type "int"; expected "str"

# :---------------------------
# :Make
# :---------------------------

# [case test_make_from_dict]
# :-------------------------
import attr
C = attr.make_class("C", {
    "x": attr.ib(type=int),
    "y": attr.ib()
})


# [case test_make_from_str]
# :------------------------
import attr
C = attr.make_class("C", ["x", "y"])


# [case test_astuple]
# :------------------
import attr
@attr.s
class C:
    a: int = attr.ib()

t1 = attr.astuple(C)
reveal_type(t1)  # E: Revealed type is 'builtins.tuple[Any]'


# [case test_asdict]
# :-----------------
import attr
@attr.s
class C:
    a: int = attr.ib()

t1 = attr.asdict(C)
reveal_type(t1)  # E: Revealed type is 'builtins.dict[builtins.str, Any]'
