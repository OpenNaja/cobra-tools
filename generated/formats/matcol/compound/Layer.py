from generated.formats.base.basic import fmt_member
from generated.array import Array
from generated.formats.base.basic import ZString
from generated.formats.matcol.compound.Attrib import Attrib
from generated.formats.matcol.compound.Info import Info
from generated.formats.matcol.compound.LayerFrag import LayerFrag
from generated.struct import StructBase


class Layer(StructBase):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.info = 0
		self.name = 0
		self.infos = 0
		self.info_names = 0
		self.attribs = 0
		self.attrib_names = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.info = LayerFrag(self.context, 0, None)
		self.name = ''
		self.infos = Array((self.info.info_count,), Info, self.context, 0, None)
		self.info_names = Array((self.info.info_count,), ZString, self.context, 0, None)
		self.attribs = Array((self.info.attrib_count,), Attrib, self.context, 0, None)
		self.attrib_names = Array((self.info.attrib_count,), ZString, self.context, 0, None)

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
		instance.info = LayerFrag.from_stream(stream, instance.context, 0, None)
		instance.name = stream.read_zstring()
		instance.infos = Array.from_stream(stream, (instance.info.info_count,), Info, instance.context, 0, None)
		instance.info_names = stream.read_zstrings((instance.info.info_count,))
		instance.attribs = Array.from_stream(stream, (instance.info.attrib_count,), Attrib, instance.context, 0, None)
		instance.attrib_names = stream.read_zstrings((instance.info.attrib_count,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		LayerFrag.to_stream(stream, instance.info)
		stream.write_zstring(instance.name)
		Array.to_stream(stream, instance.infos, (instance.info.info_count,), Info, instance.context, 0, None)
		stream.write_zstrings(instance.info_names)
		Array.to_stream(stream, instance.attribs, (instance.info.attrib_count,), Attrib, instance.context, 0, None)
		stream.write_zstrings(instance.attrib_names)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('info', LayerFrag, (0, None))
		yield ('name', ZString, (0, None))
		yield ('infos', Array, ((instance.info.info_count,), Info, 0, None))
		yield ('info_names', Array, ((instance.info.info_count,), ZString, 0, None))
		yield ('attribs', Array, ((instance.info.attrib_count,), Attrib, 0, None))
		yield ('attrib_names', Array, ((instance.info.attrib_count,), ZString, 0, None))

	def get_info_str(self, indent=0):
		return f'Layer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* info = {fmt_member(self.info, indent+1)}'
		s += f'\n	* name = {fmt_member(self.name, indent+1)}'
		s += f'\n	* infos = {fmt_member(self.infos, indent+1)}'
		s += f'\n	* info_names = {fmt_member(self.info_names, indent+1)}'
		s += f'\n	* attribs = {fmt_member(self.attribs, indent+1)}'
		s += f'\n	* attrib_names = {fmt_member(self.attrib_names, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
