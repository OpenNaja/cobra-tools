from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class AuxEntry(BaseStruct):

	"""
	describes an external AUX resource
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into files list
		self.file_index = 0

		# offset for suffix into string name table
		self.offset = 0

		# byte count of the complete external resource file
		self.size = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.file_index = 0
		self.offset = 0
		self.size = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.file_index = Uint.from_stream(stream, instance.context, 0, None)
		instance.offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.size = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.file_index)
		Uint.to_stream(stream, instance.offset)
		Uint.to_stream(stream, instance.size)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'file_index', Uint, (0, None), (False, None)
		yield 'offset', Uint, (0, None), (False, None)
		yield 'size', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'AuxEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* file_index = {self.fmt_member(self.file_index, indent+1)}'
		s += f'\n	* offset = {self.fmt_member(self.offset, indent+1)}'
		s += f'\n	* size = {self.fmt_member(self.size, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
