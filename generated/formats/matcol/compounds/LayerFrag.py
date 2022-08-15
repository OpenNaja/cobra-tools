import generated.formats.base.basic
import generated.formats.matcol.compounds.Attrib
import generated.formats.matcol.compounds.Info
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LayerFrag(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.u_1 = 0
		self.info_count = 0
		self.u_2 = 0
		self.u_3 = 0
		self.attrib_count = 0
		self.layer_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.infos = ArrayPointer(self.context, self.info_count, generated.formats.matcol.compounds.Info.Info)
		self.attribs = ArrayPointer(self.context, self.attrib_count, generated.formats.matcol.compounds.Attrib.Attrib)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.u_0 = 0
		self.u_1 = 0
		self.info_count = 0
		self.u_2 = 0
		self.u_3 = 0
		self.attrib_count = 0
		self.layer_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.infos = ArrayPointer(self.context, self.info_count, generated.formats.matcol.compounds.Info.Info)
		self.attribs = ArrayPointer(self.context, self.attrib_count, generated.formats.matcol.compounds.Attrib.Attrib)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.layer_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.u_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.infos = ArrayPointer.from_stream(stream, instance.context, instance.info_count, generated.formats.matcol.compounds.Info.Info)
		instance.info_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.u_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.u_3 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.attribs = ArrayPointer.from_stream(stream, instance.context, instance.attrib_count, generated.formats.matcol.compounds.Attrib.Attrib)
		instance.attrib_count = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.layer_name, int):
			instance.layer_name.arg = 0
		if not isinstance(instance.infos, int):
			instance.infos.arg = instance.info_count
		if not isinstance(instance.attribs, int):
			instance.attribs.arg = instance.attrib_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.layer_name)
		stream.write_uint64(instance.u_0)
		stream.write_uint64(instance.u_1)
		ArrayPointer.to_stream(stream, instance.infos)
		stream.write_uint64(instance.info_count)
		stream.write_uint64(instance.u_2)
		stream.write_uint64(instance.u_3)
		ArrayPointer.to_stream(stream, instance.attribs)
		stream.write_uint64(instance.attrib_count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'layer_name', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'u_0', Uint64, (0, None)
		yield 'u_1', Uint64, (0, None)
		yield 'infos', ArrayPointer, (instance.info_count, generated.formats.matcol.compounds.Info.Info)
		yield 'info_count', Uint64, (0, None)
		yield 'u_2', Uint64, (0, None)
		yield 'u_3', Uint64, (0, None)
		yield 'attribs', ArrayPointer, (instance.attrib_count, generated.formats.matcol.compounds.Attrib.Attrib)
		yield 'attrib_count', Uint64, (0, None)

	def get_info_str(self, indent=0):
		return f'LayerFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* layer_name = {self.fmt_member(self.layer_name, indent+1)}'
		s += f'\n	* u_0 = {self.fmt_member(self.u_0, indent+1)}'
		s += f'\n	* u_1 = {self.fmt_member(self.u_1, indent+1)}'
		s += f'\n	* infos = {self.fmt_member(self.infos, indent+1)}'
		s += f'\n	* info_count = {self.fmt_member(self.info_count, indent+1)}'
		s += f'\n	* u_2 = {self.fmt_member(self.u_2, indent+1)}'
		s += f'\n	* u_3 = {self.fmt_member(self.u_3, indent+1)}'
		s += f'\n	* attribs = {self.fmt_member(self.attribs, indent+1)}'
		s += f'\n	* attrib_count = {self.fmt_member(self.attrib_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
