from generated.array import Array
from generated.formats.motiongraph.compounds.XMLEntry import XMLEntry
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class XMLArray(MemStruct):

	__name__ = 'XMLArray'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.xmls = Array((0,), XMLEntry, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.xmls = Array((self.arg,), XMLEntry, self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.xmls = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), XMLEntry)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.xmls, (instance.arg,), XMLEntry, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'xmls', Array, ((instance.arg,), XMLEntry, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'XMLArray [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* xmls = {self.fmt_member(self.xmls, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
