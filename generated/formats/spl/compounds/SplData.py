from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.spl.compounds.Key import Key
from generated.formats.spl.compounds.Vector3 import Vector3


class SplData(MemStruct):

	"""
	JWE2: 16 + n*16 bytes
	"""

	__name__ = 'SplData'

	_import_path = 'generated.formats.spl.compounds.SplData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.offset = Vector3(self.context, 0, None)
		self.scale = 0.0
		self.keys = Array(self.context, 0, None, (0,), Key)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.offset = Vector3(self.context, 0, None)
		self.scale = 0.0
		self.keys = Array(self.context, 0, None, (self.arg,), Key)

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
		Float.to_stream(stream, instance.scale)
		Array.to_stream(stream, instance.keys, instance.context, 0, None, (instance.arg,), Key)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', Vector3, (0, None), (False, None)
		yield 'scale', Float, (0, None), (False, None)
		yield 'keys', Array, (0, None, (instance.arg,), Key), (False, None)

	def get_info_str(self, indent=0):
		return f'SplData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
