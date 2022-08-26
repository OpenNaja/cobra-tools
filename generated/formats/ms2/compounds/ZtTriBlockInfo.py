from generated.base_struct import BaseStruct
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint


class ZtTriBlockInfo(BaseStruct):

	"""
	8 bytes total
	"""

	__name__ = 'ZtTriBlockInfo'

	_import_path = 'generated.formats.ms2.compounds.ZtTriBlockInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.tri_index_count = 0
		self.a = 0
		self.unk_index = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.tri_index_count = 0
		self.a = 0
		self.unk_index = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.tri_index_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.a = Short.from_stream(stream, instance.context, 0, None)
		instance.unk_index = Short.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.tri_index_count)
		Short.to_stream(stream, instance.a)
		Short.to_stream(stream, instance.unk_index)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'tri_index_count', Uint, (0, None), (False, None)
		yield 'a', Short, (0, None), (False, None)
		yield 'unk_index', Short, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ZtTriBlockInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* tri_index_count = {self.fmt_member(self.tri_index_count, indent+1)}'
		s += f'\n	* a = {self.fmt_member(self.a, indent+1)}'
		s += f'\n	* unk_index = {self.fmt_member(self.unk_index, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
