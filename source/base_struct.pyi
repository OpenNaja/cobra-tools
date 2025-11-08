

from typing import Any, ClassVar
from generated.context import ContextReference

class StructMetaClass(type):
    pass

class BaseStruct:

    context: ClassVar[ContextReference]

    _attribute_list: ClassVar[set]
    allow_np: ClassVar[bool]

    name: str
    _context: ContextReference
    arg: Any
    template: Any
    io_size: int
    io_start: int

    def __init__(self, context: Any, arg: Any, template: Any, set_default: bool): ...
