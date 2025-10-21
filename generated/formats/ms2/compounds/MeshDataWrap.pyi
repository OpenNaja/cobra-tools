from typing import Union
from generated.formats.ms2.compounds.ChunkedMesh import ChunkedMesh
from generated.formats.ms2.compounds.NewMeshData import NewMeshData
from generated.formats.ms2.compounds.PcMeshData import PcMeshData
from generated.formats.ms2.compounds.ZtMeshData import ZtMeshData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MeshDataWrap(MemStruct):
    mesh: Union[ChunkedMesh, NewMeshData, PcMeshData, ZtMeshData]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
