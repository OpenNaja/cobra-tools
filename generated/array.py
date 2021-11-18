from operator import index
from math import prod

from generated.context import ContextReference


class Array(list):
    '''Main class responsible for creating, reading and storing (nested) lists of the custom data types, functioning
    mostly like an array.
    '''

    context = ContextReference()

    def __new__(cls, shape, dtype, context, arg=None, template=None, set_default=True):
        if callable(getattr(dtype, 'create_array', None)):
            # there is a more efficient method of creating this array on the class (which may not return Array class type)
            return dtype.create_array(shape, None, context, arg, template)
        else:
            return super(cls, cls).__new__(cls)

    def __init__(self, shape, dtype, context, arg=None, template=None, set_default=True):
        '''Create a new array of the specified shape and type.
        :param shape: Shape of the resulting array. Zero-dimensional arrays are not supported.
        :type shape: Union[int, Tuple[int, ...]]
        :param dtype: The class to use for instancing objects in this array. If it supports create_array, that will 
        be used instead.
        :type dtype: type
        :param context: The context object to use for this array (necessary for version and other global conditions).
        :type context: Any object which supports accessing for global conditions.
        :param arg: 'arg' parameter to use for instancing objects in this array.
        :param template: 'template' parameter to use for instancing objects in this array.
        :param set_default: Whether to create the elements of this array on init. If false, it is assumed that these
        elements will be created by another process immediately after init.
        :type set_default: bool, optional
        '''
        super().__init__(self)
        self.shape = shape
        self.ndim = len(self.shape)
        self.dtype = dtype
        self._context = context
        self.arg = arg
        self.template = template
        if set_default:
            self.set_defaults()

    def test(self):
        self.__init__()

    def set_defaults(self):
        self[:] = self.create_nested_list(lambda : self.dtype(self.context, self.arg, self.template), self.shape)

    def read(self, stream):
        self.io_start = stream.tell()
        self[:] = self.create_nested_list(lambda : self.dtype.from_stream(stream, self.context, self.arg, self.template), self.shape)
        self.io_size = stream.tell() - self.io_start

    def write(self, stream):
        self.io_start = stream.tell()
        self.perform_nested_func(self, lambda x: self.dtype.to_stream(stream, x), self.ndim)
        self.io_size = stream.tell() - self.io_start


    @classmethod
    def from_stream(cls, stream, shape, dtype, context, arg=None, template=None):
        if callable(getattr(dtype, 'read_array', None)):
            return dtype.read_array(stream, shape, context, arg, template)
        else:
            new_array = cls(shape, dtype, context, arg, template, set_default=False)
            
            new_array.read(stream, shape, dtype, context, arg, template)
            return new_array

    @classmethod
    def to_stream(cls, stream, instance, shape, dtype, context, arg=None, template=None):
        if callable(getattr(dtype, 'write_array', None)):
            dtype.write_array(stream, instance)
        else:
            instance.store_params(shape, dtype, context, arg, template)
            instance.write(stream)

    @classmethod
    def from_value(cls, shape, dtype, value):
        if callable(getattr(dtype, 'create_array', None)):
            return dtype.create_array(shape, default=value)
        else:
            new_array = cls(shape, dtype, None, set_default=False)
            new_array[:] = cls.create_nested_list(lambda : dtype.from_value(value), shape)
            return new_array

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape_input):
        # conversion to int happens using the 'index' operator
        try:
            # try to convert iterable to a tuple of ints
            shape = tuple(index(i) for i in shape_input)
        except TypeError:
            # if this can't be converted to a tuple, try instead to convert an integer-like to (int, )
            shape = (index(shape_input), )
        self._shape = shape

    @property
    def ndim(self):
        return len(self.shape)
        

    @property
    def size(self):
        return prod(self.shape)

    @classmethod
    def create_nested_list(cls, function_to_generate, shape):
		# create a nested list with the specified shape, where every element is created by function_to_generate()
        if len(shape) > 1:
            return [cls.create_nested_list(function_to_generate, shape[1:]) for _ in range(shape[0])]
        else:
            return [function_to_generate() for _ in range(shape[0])]

    @classmethod
    def perform_nested_func(cls, nested_iterable, efunc, ndim):
        # perform a function efunc(element) on every element in a nested iterable and return the result
        if ndim > 1:
            return [cls.perform_nested_func(sublist, efunc, ndim - 1) for sublist in nested_iterable]
        else:
            return [efunc(element) for element in nested_iterable]

    def store_params(self, shape, dtype, context, arg, template):
        self.shape = shape
        self.dtype = dtype
        self._context = context
        self.arg = arg
        self.template = template
