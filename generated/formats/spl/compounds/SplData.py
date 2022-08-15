from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.spl.compounds.Key import Key
from generated.formats.spl.compounds.Vector3 import Vector3


class SplData(MemStruct):

	"""
	JWE2: 16 + n*16 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.offset = Vector3(self.context, 0, None)
		self.scale = 0.0
		self.keys = Array((self.arg,), Key, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.offset = Vector3(self.context, 0, None)
		self.scale = 0.0
		self.keys = Array((self.arg,), Key, self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.offset = Vector3.from_stream(stream, instance.context, 0, None)
		instance.scale = Float.from_stream(stream, instance.context, 0, None)
		instance.keys = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), Key)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Vector3.to_stream(stream, instance.offset)
		stream.write_float(instance.scale)
		Array.to_stream(stream, instance.keys, (instance.arg,), Key, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'offset', Vector3, (0, None)
		yield 'scale', Float, (0, None)
		yield 'keys', Array, ((instance.arg,), Key, 0, None)

	def get_info_str(self, indent=0):
		return f'SplData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* offset = {self.fmt_member(self.offset, indent+1)}'
		s += f'\n	* scale = {self.fmt_member(self.scale, indent+1)}'
		s += f'\n	* keys = {self.fmt_member(self.keys, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
