from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.bnk.compounds.HircPointer import HircPointer


class HIRCSection(BaseStruct):

	"""
	The HIRC section contains all the Wwise objects, including the events, the containers to group sounds, and the references to the sound files.
	"""

	__name__ = HIRCSection

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of following data
		self.length = 0
		self.count = 0
		self.hirc_pointers = Array((0,), HircPointer, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.length = 0
		self.count = 0
		self.hirc_pointers = Array((self.count,), HircPointer, self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.length = Uint.from_stream(stream, instance.context, 0, None)
		instance.count = Uint.from_stream(stream, instance.context, 0, None)
		instance.hirc_pointers = Array.from_stream(stream, instance.context, 0, None, (instance.count,), HircPointer)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.length)
		Uint.to_stream(stream, instance.count)
		Array.to_stream(stream, instance.hirc_pointers, (instance.count,), HircPointer, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'length', Uint, (0, None), (False, None)
		yield 'count', Uint, (0, None), (False, None)
		yield 'hirc_pointers', Array, ((instance.count,), HircPointer, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'HIRCSection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* length = {self.fmt_member(self.length, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* hirc_pointers = {self.fmt_member(self.hirc_pointers, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
