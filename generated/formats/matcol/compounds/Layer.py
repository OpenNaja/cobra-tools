from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import ZString
from generated.formats.matcol.compounds.Attrib import Attrib
from generated.formats.matcol.compounds.Info import Info
from generated.formats.matcol.compounds.LayerFrag import LayerFrag


class Layer(BaseStruct):

	__name__ = 'Layer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.info = LayerFrag(self.context, 0, None)
		self.name = ''
		self.infos = Array((0,), Info, self.context, 0, None)
		self.info_names = Array((0,), ZString, self.context, 0, None)
		self.attribs = Array((0,), Attrib, self.context, 0, None)
		self.attrib_names = Array((0,), ZString, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.info = LayerFrag(self.context, 0, None)
		self.name = ''
		self.infos = Array((self.info.info_count,), Info, self.context, 0, None)
		self.info_names = Array((self.info.info_count,), ZString, self.context, 0, None)
		self.attribs = Array((self.info.attrib_count,), Attrib, self.context, 0, None)
		self.attrib_names = Array((self.info.attrib_count,), ZString, self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.info = LayerFrag.from_stream(stream, instance.context, 0, None)
		instance.name = ZString.from_stream(stream, instance.context, 0, None)
		instance.infos = Array.from_stream(stream, instance.context, 0, None, (instance.info.info_count,), Info)
		instance.info_names = Array.from_stream(stream, instance.context, 0, None, (instance.info.info_count,), ZString)
		instance.attribs = Array.from_stream(stream, instance.context, 0, None, (instance.info.attrib_count,), Attrib)
		instance.attrib_names = Array.from_stream(stream, instance.context, 0, None, (instance.info.attrib_count,), ZString)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		LayerFrag.to_stream(stream, instance.info)
		ZString.to_stream(stream, instance.name)
		Array.to_stream(stream, instance.infos, (instance.info.info_count,), Info, instance.context, 0, None)
		Array.to_stream(stream, instance.info_names, (instance.info.info_count,), ZString, instance.context, 0, None)
		Array.to_stream(stream, instance.attribs, (instance.info.attrib_count,), Attrib, instance.context, 0, None)
		Array.to_stream(stream, instance.attrib_names, (instance.info.attrib_count,), ZString, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'info', LayerFrag, (0, None), (False, None)
		yield 'name', ZString, (0, None), (False, None)
		yield 'infos', Array, ((instance.info.info_count,), Info, 0, None), (False, None)
		yield 'info_names', Array, ((instance.info.info_count,), ZString, 0, None), (False, None)
		yield 'attribs', Array, ((instance.info.attrib_count,), Attrib, 0, None), (False, None)
		yield 'attrib_names', Array, ((instance.info.attrib_count,), ZString, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Layer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* info = {self.fmt_member(self.info, indent+1)}'
		s += f'\n	* name = {self.fmt_member(self.name, indent+1)}'
		s += f'\n	* infos = {self.fmt_member(self.infos, indent+1)}'
		s += f'\n	* info_names = {self.fmt_member(self.info_names, indent+1)}'
		s += f'\n	* attribs = {self.fmt_member(self.attribs, indent+1)}'
		s += f'\n	* attrib_names = {self.fmt_member(self.attrib_names, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
