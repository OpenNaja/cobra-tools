from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class SetEntry(BaseStruct):

	"""
	the asset indices of two consecutive SetEntries define a set of AssetEntries
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.file_hash = 0
		self.ext_hash = 0

		# add from last set's entry up to this index to this set
		self.start = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.file_hash = 0
		if self.context.version >= 19:
			self.ext_hash = 0
		self.start = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.file_hash = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 19:
			instance.ext_hash = Uint.from_stream(stream, instance.context, 0, None)
		instance.start = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.file_hash)
		if instance.context.version >= 19:
			Uint.to_stream(stream, instance.ext_hash)
		Uint.to_stream(stream, instance.start)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'file_hash', Uint, (0, None)
		if instance.context.version >= 19:
			yield 'ext_hash', Uint, (0, None)
		yield 'start', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'SetEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* file_hash = {self.fmt_member(self.file_hash, indent+1)}'
		s += f'\n	* ext_hash = {self.fmt_member(self.ext_hash, indent+1)}'
		s += f'\n	* start = {self.fmt_member(self.start, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
