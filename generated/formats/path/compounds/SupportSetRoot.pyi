from generated.array import Array
from generated.formats.base.compounds.Vector2 import Vector2
from generated.formats.base.compounds.Vector3 import Vector3
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.CondPointer import CondPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.path.compounds.BrokeStruct import BrokeStruct
from generated.formats.path.compounds.Connector import Connector
from generated.formats.path.compounds.ConnectorMultiJoint import ConnectorMultiJoint
from generated.formats.path.compounds.Footer import Footer
from generated.formats.path.compounds.Pillar import Pillar
from generated.formats.path.compounds.SubBrace import SubBrace
from generated.formats.path.compounds.SupportSetData import SupportSetData


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
