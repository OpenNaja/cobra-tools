from typing import Union
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.ms2.compounds.DLAPreBones import DLAPreBones
from generated.formats.ms2.compounds.FloatsY import FloatsY
from generated.formats.ms2.compounds.LodInfo import LodInfo
from generated.formats.ms2.compounds.MaterialName import MaterialName
from generated.formats.ms2.compounds.MeshDataWrap import MeshDataWrap
from generated.formats.ms2.compounds.Object import Object
from generated.formats.ms2.compounds.ZTPreBones import ZTPreBones
from generated.formats.ovl_base.compounds.Empty import Empty


class Model(BaseStruct):
    start_ref: Empty
    materials: Array[MaterialName]
    lods: Array[LodInfo]
    objects: Array[Object]
    mesh_aligner: PadAlign[object]
    meshes: Array[MeshDataWrap]
    pre_bones: Union[DLAPreBones, ZTPreBones]
    floatsy: Array[FloatsY]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
