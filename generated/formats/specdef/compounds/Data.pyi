from typing import Union
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.specdef.compounds.ArrayData import ArrayData
from generated.formats.specdef.compounds.BooleanData import BooleanData
from generated.formats.specdef.compounds.ChildSpecData import ChildSpecData
from generated.formats.specdef.compounds.FloatData import FloatData
from generated.formats.specdef.compounds.Int16Data import Int16Data
from generated.formats.specdef.compounds.Int32Data import Int32Data
from generated.formats.specdef.compounds.Int64Data import Int64Data
from generated.formats.specdef.compounds.Int8Data import Int8Data
from generated.formats.specdef.compounds.ReferenceToObjectData import ReferenceToObjectData
from generated.formats.specdef.compounds.StringData import StringData
from generated.formats.specdef.compounds.Uint16Data import Uint16Data
from generated.formats.specdef.compounds.Uint32Data import Uint32Data
from generated.formats.specdef.compounds.Uint64Data import Uint64Data
from generated.formats.specdef.compounds.Uint8Data import Uint8Data
from generated.formats.specdef.compounds.Vector2 import Vector2
from generated.formats.specdef.compounds.Vector3 import Vector3


class Data(MemStruct):
    dtype: Union[ArrayData, BooleanData, ChildSpecData, FloatData, Int16Data, Int32Data, Int64Data, Int8Data, ReferenceToObjectData, StringData, Uint16Data, Uint32Data, Uint64Data, Uint8Data, Vector2, Vector3]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
