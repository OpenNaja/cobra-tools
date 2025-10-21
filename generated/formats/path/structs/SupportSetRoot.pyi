from generated.array import Array
from generated.formats.base.structs.Vector2 import Vector2
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.CondPointer import CondPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.path.structs.BrokeStruct import BrokeStruct
from generated.formats.path.structs.Connector import Connector
from generated.formats.path.structs.ConnectorMultiJoint import ConnectorMultiJoint
from generated.formats.path.structs.Footer import Footer
from generated.formats.path.structs.Pillar import Pillar
from generated.formats.path.structs.SubBrace import SubBrace
from generated.formats.path.structs.SupportSetData import SupportSetData


class SupportSetRoot(MemStruct):
    connector_1: ArrayPointer[Connector]
    connector_2: ArrayPointer[ConnectorMultiJoint]
    pillar: ArrayPointer[Pillar]
    footer: ArrayPointer[Footer]
    sub_braces: ArrayPointer[SubBrace]
    unk_vector_1: Vector3
    unk_vector_2: Vector2
    unk_vector_3: Vector3
    unk_int_1: int
    num_connector_1: int
    num_connector_2: int
    num_pillar: int
    num_footer: int
    num_sub_brace: int
    unk_floats: Array[float]
    broken_supports: CondPointer[BrokeStruct]
    data: ArrayPointer[SupportSetData]
    num_data: int
    zeros: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
