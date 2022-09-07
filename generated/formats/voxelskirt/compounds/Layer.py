from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class Layer(BaseStruct):

	"""
	32 bytes
	PZ and JWE only, describes a data layer image
	"""

	__name__ = 'Layer'

	_import_path = 'generated.formats.voxelskirt.compounds.Layer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into name list
		self.id = 0

		# 0 = ubyte, 2 = float
		self.dtype = 0

		# address of this data layer
		self.offset = 0

		# data size of this layer, in bytes
		self.dsize = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.id = 0
		# leaving self.dtype alone
		self.offset = 0
		self.dsize = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.id = Uint64.from_stream(stream, instance.context, 0, None)
		instance.dtype = Uint64.from_stream(stream, instance.context, 0, None)
		instance.offset = Uint64.from_stream(stream, instance.context, 0, None)
		instance.dsize = Uint64.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.id)
		Uint64.to_stream(stream, instance.dtype)
		Uint64.to_stream(stream, instance.offset)
		Uint64.to_stream(stream, instance.dsize)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'id', Uint64, (0, None), (False, None)
		yield 'dtype', Uint64, (0, None), (False, None)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'dsize', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Layer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* id = {self.fmt_member(self.id, indent+1)}'
		s += f'\n	* dtype = {self.fmt_member(self.dtype, indent+1)}'
		s += f'\n	* offset = {self.fmt_member(self.offset, indent+1)}'
		s += f'\n	* dsize = {self.fmt_member(self.dsize, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
