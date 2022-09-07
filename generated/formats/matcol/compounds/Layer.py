from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import ZString
from generated.formats.matcol.compounds.Attrib import Attrib
from generated.formats.matcol.compounds.Info import Info
from generated.formats.matcol.compounds.LayerFrag import LayerFrag


class Layer(BaseStruct):

	__name__ = 'Layer'

	_import_path = 'generated.formats.matcol.compounds.Layer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.info = LayerFrag(self.context, 0, None)
		self.name = ''
		self.infos = Array(self.context, 0, None, (0,), Info)
		self.info_names = Array(self.context, 0, None, (0,), ZString)
		self.attribs = Array(self.context, 0, None, (0,), Attrib)
		self.attrib_names = Array(self.context, 0, None, (0,), ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.info = LayerFrag(self.context, 0, None)
		self.name = ''
		self.infos = Array(self.context, 0, None, (self.info.info_count,), Info)
		self.info_names = Array(self.context, 0, None, (self.info.info_count,), ZString)
		self.attribs = Array(self.context, 0, None, (self.info.attrib_count,), Attrib)
		self.attrib_names = Array(self.context, 0, None, (self.info.attrib_count,), ZString)

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
		Array.to_stream(stream, instance.infos, instance.context, 0, None, (instance.info.info_count,), Info)
		Array.to_stream(stream, instance.info_names, instance.context, 0, None, (instance.info.info_count,), ZString)
		Array.to_stream(stream, instance.attribs, instance.context, 0, None, (instance.info.attrib_count,), Attrib)
		Array.to_stream(stream, instance.attrib_names, instance.context, 0, None, (instance.info.attrib_count,), ZString)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'info', LayerFrag, (0, None), (False, None)
		yield 'name', ZString, (0, None), (False, None)
		yield 'infos', Array, (0, None, (instance.info.info_count,), Info), (False, None)
		yield 'info_names', Array, (0, None, (instance.info.info_count,), ZString), (False, None)
		yield 'attribs', Array, (0, None, (instance.info.attrib_count,), Attrib), (False, None)
		yield 'attrib_names', Array, (0, None, (instance.info.attrib_count,), ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'Layer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
