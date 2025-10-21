from typing import Union
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.specdef.structs.ArrayData import ArrayData
from generated.formats.specdef.structs.BooleanData import BooleanData
from generated.formats.specdef.structs.ChildSpecData import ChildSpecData
from generated.formats.specdef.structs.FloatData import FloatData
from generated.formats.specdef.structs.Int16Data import Int16Data
from generated.formats.specdef.structs.Int32Data import Int32Data
from generated.formats.specdef.structs.Int64Data import Int64Data
from generated.formats.specdef.structs.Int8Data import Int8Data
from generated.formats.specdef.structs.ReferenceToObjectData import ReferenceToObjectData
from generated.formats.specdef.structs.StringData import StringData
from generated.formats.specdef.structs.Uint16Data import Uint16Data
from generated.formats.specdef.structs.Uint32Data import Uint32Data
from generated.formats.specdef.structs.Uint64Data import Uint64Data
from generated.formats.specdef.structs.Uint8Data import Uint8Data
from generated.formats.specdef.structs.Vector2 import Vector2
from generated.formats.specdef.structs.Vector3 import Vector3


class Data(MemStruct):
    dtype: Union[ArrayData, BooleanData, ChildSpecData, FloatData, Int16Data, Int32Data, Int64Data, Int8Data, ReferenceToObjectData, StringData, Uint16Data, Uint32Data, Uint64Data, Uint8Data, Vector2, Vector3]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
