from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint64
from generated.formats.fct.compounds.Font import Font
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FctRoot(MemStruct):

	"""
	JWE1: 104 bytes
	"""

	__name__ = 'FctRoot'

	_import_path = 'generated.formats.fct.compounds.FctRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.u_1 = 0
		self.a = 0.0
		self.b = 0.0
		self.c = 0.0
		self.minus_1 = 0
		self.z_0 = 0
		self.z_1 = 0
		self.z_2 = 0
		self.offset = 0
		self.fonts = Array(self.context, 0, None, (0,), Font)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.u_0 = 0
		self.u_1 = 0
		self.a = 0.0
		self.b = 0.0
		self.c = 0.0
		self.minus_1 = 0
		self.z_0 = 0
		self.z_1 = 0
		self.z_2 = 0
		self.offset = 0
		self.fonts = Array(self.context, 0, None, (4,), Font)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.u_0 = Short.from_stream(stream, instance.context, 0, None)
		instance.u_1 = Short.from_stream(stream, instance.context, 0, None)
		instance.a = Float.from_stream(stream, instance.context, 0, None)
		instance.b = Float.from_stream(stream, instance.context, 0, None)
		instance.c = Float.from_stream(stream, instance.context, 0, None)
		instance.minus_1 = Short.from_stream(stream, instance.context, 0, None)
		instance.z_0 = Short.from_stream(stream, instance.context, 0, None)
		instance.z_1 = Int.from_stream(stream, instance.context, 0, None)
		instance.z_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.offset = Uint64.from_stream(stream, instance.context, 0, None)
		instance.fonts = Array.from_stream(stream, instance.context, 0, None, (4,), Font)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Short.to_stream(stream, instance.u_0)
		Short.to_stream(stream, instance.u_1)
		Float.to_stream(stream, instance.a)
		Float.to_stream(stream, instance.b)
		Float.to_stream(stream, instance.c)
		Short.to_stream(stream, instance.minus_1)
		Short.to_stream(stream, instance.z_0)
		Int.to_stream(stream, instance.z_1)
		Uint64.to_stream(stream, instance.z_2)
		Uint64.to_stream(stream, instance.offset)
		Array.to_stream(stream, instance.fonts, instance.context, 0, None, (4,), Font)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'u_0', Short, (0, None), (False, None)
		yield 'u_1', Short, (0, None), (False, None)
		yield 'a', Float, (0, None), (False, None)
		yield 'b', Float, (0, None), (False, None)
		yield 'c', Float, (0, None), (False, None)
		yield 'minus_1', Short, (0, None), (False, None)
		yield 'z_0', Short, (0, None), (False, None)
		yield 'z_1', Int, (0, None), (False, None)
		yield 'z_2', Uint64, (0, None), (False, None)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'fonts', Array, (0, None, (4,), Font), (False, None)

	def get_info_str(self, indent=0):
		return f'FctRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
