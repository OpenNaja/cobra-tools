from generated.array import Array
from generated.formats.ms2.compounds.Matrix import Matrix


class Matrix44(Matrix):
    data: Array[Array[float]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
