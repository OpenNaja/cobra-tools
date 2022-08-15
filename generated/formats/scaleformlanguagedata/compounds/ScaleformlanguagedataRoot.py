import generated.formats.scaleformlanguagedata.compounds.FontInfo
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ScaleformlanguagedataRoot(MemStruct):

	"""
	# PC - is maybe organized differently here
	PZ: 48 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_0 = 0
		self.zero_1 = 0
		self.count = 0
		self.zero_2 = 0
		self.zero_3 = 0
		self.fonts = ArrayPointer(self.context, self.count, generated.formats.scaleformlanguagedata.compounds.FontInfo.FontInfo)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zero_0 = 0
		self.zero_1 = 0
		self.count = 0
		self.zero_2 = 0
		self.zero_3 = 0
		self.fonts = ArrayPointer(self.context, self.count, generated.formats.scaleformlanguagedata.compounds.FontInfo.FontInfo)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zero_0 = stream.read_uint64()
		instance.zero_1 = stream.read_uint64()
		instance.fonts = ArrayPointer.from_stream(stream, instance.context, instance.count, generated.formats.scaleformlanguagedata.compounds.FontInfo.FontInfo)
		instance.count = stream.read_uint64()
		instance.zero_2 = stream.read_uint64()
		instance.zero_3 = stream.read_uint64()
		if not isinstance(instance.fonts, int):
			instance.fonts.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.zero_0)
		stream.write_uint64(instance.zero_1)
		ArrayPointer.to_stream(stream, instance.fonts)
		stream.write_uint64(instance.count)
		stream.write_uint64(instance.zero_2)
		stream.write_uint64(instance.zero_3)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'zero_0', Uint64, (0, None)
		yield 'zero_1', Uint64, (0, None)
		yield 'fonts', ArrayPointer, (instance.count, generated.formats.scaleformlanguagedata.compounds.FontInfo.FontInfo)
		yield 'count', Uint64, (0, None)
		yield 'zero_2', Uint64, (0, None)
		yield 'zero_3', Uint64, (0, None)

	def get_info_str(self, indent=0):
		return f'ScaleformlanguagedataRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* fonts = {self.fmt_member(self.fonts, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* zero_2 = {self.fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* zero_3 = {self.fmt_member(self.zero_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
