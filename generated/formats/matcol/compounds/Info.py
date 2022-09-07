import numpy
from generated.array import Array
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Info(MemStruct):

	__name__ = 'Info'

	_import_path = 'generated.formats.matcol.compounds.Info'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flags = Array(self.context, 0, None, (0,), Byte)
		self.value = Array(self.context, 0, None, (0,), Float)
		self.padding = 0
		self.info_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.flags = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.value = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.padding = 0
		self.info_name = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.info_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.flags = Array.from_stream(stream, instance.context, 0, None, (4,), Byte)
		instance.value = Array.from_stream(stream, instance.context, 0, None, (4,), Float)
		instance.padding = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.info_name, int):
			instance.info_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.info_name)
		Array.to_stream(stream, instance.flags, instance.context, 0, None, (4,), Byte)
		Array.to_stream(stream, instance.value, instance.context, 0, None, (4,), Float)
		Uint.to_stream(stream, instance.padding)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'info_name', Pointer, (0, ZString), (False, None)
		yield 'flags', Array, (0, None, (4,), Byte), (False, None)
		yield 'value', Array, (0, None, (4,), Float), (False, None)
		yield 'padding', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Info [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
