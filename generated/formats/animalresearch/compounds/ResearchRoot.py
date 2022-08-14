import generated.formats.animalresearch.compounds.ResearchLevel
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ResearchRoot(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.levels = ArrayPointer(self.context, self.count, generated.formats.animalresearch.compounds.ResearchLevel.ResearchLevel)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.levels = ArrayPointer(self.context, self.count, generated.formats.animalresearch.compounds.ResearchLevel.ResearchLevel)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.levels = ArrayPointer.from_stream(stream, instance.context, instance.count, generated.formats.animalresearch.compounds.ResearchLevel.ResearchLevel)
		instance.count = stream.read_uint64()
		if not isinstance(instance.levels, int):
			instance.levels.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.levels)
		stream.write_uint64(instance.count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'levels', ArrayPointer, (instance.count, generated.formats.animalresearch.compounds.ResearchLevel.ResearchLevel)
		yield 'count', Uint64, (0, None)

	def get_info_str(self, indent=0):
		return f'ResearchRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* levels = {self.fmt_member(self.levels, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
