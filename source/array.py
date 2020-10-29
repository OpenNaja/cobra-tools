class Array(list):

    def __init__(self, default=()):
        super().__init__(self)
        if default:
            self.extend(default)
        self.dtype = None
        self.arr1 = 0
        self.arr2 = 0
        self.arg = None
        self.template = None

    def get_rfunc(self, stream, mode="read"):
        if not self.dtype:
            raise NotImplementedError("Dtype has not been set for array!")

        if isinstance(self.dtype, str):
            # print("string dtype", self.dtype)
            # for the basic types, dtype is a string
            return stream.get_io_func(self.dtype, mode=mode)
        else:
            # print("object dtype", self.dtype)
            # it is a class
            if mode == "read":
                def func():
                    return stream.read_type(self.dtype, (self.arg, self.template))
            else:
                def func(obj):
                    return stream.write_type(obj)
            return func

    def store_params(self, dtype, arr1, arr2, arg, template):
        if dtype:
            self.dtype = dtype
        self.arr1 = arr1
        self.arr2 = arr2
        self.arg = arg
        self.template = template

    def read(self, stream, dtype=None, arr1=0, arr2=None, arg=None, template=None):
        self.store_params(dtype, arr1, arr2, arg, template)
        rfunc = self.get_rfunc(stream)
        self.clear()
        if self.arr2 is None:
            self.extend([rfunc() for _ in range(self.arr1)])
        else:
            self.extend([[rfunc() for _ in range(self.arr2)] for _ in range(self.arr1)])

    def write(self, stream, dtype=None, arr1=0, arr2=None, arg=None, template=None):
        self.store_params(dtype, arr1, arr2, arg, template)
        rfunc = self.get_rfunc(stream, mode="write")
        if self.arr2 is None:
            for x in self:
                rfunc(x)
        else:
            for x in self:
                for y in x:
                    rfunc(y)


if __name__ == "__main__":
    from generated.io import BinaryStream as Bs
    from generated.formats.ovl.compound.HeaderPointer import HeaderPointer

    with Bs(b"asdasdasdasdasdsdsadasdsadsasd") as f:
        array = Array()
        # array.read(f, "Ubyte", 3, 2)
        array.read(f, HeaderPointer, 1, 2)
        print(array)

        with Bs() as b:
            array.write(b)
            print(b.getvalue())
