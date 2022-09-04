from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LayerFrag(MemStruct):

	__name__ = 'LayerFrag'

	_import_path = 'generated.formats.matcol.compounds.LayerFrag'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.u_1 = 0
		self.info_count = 0
		self.u_2 = 0
		self.u_3 = 0
		self.attrib_count = 0
		self.layer_name = Pointer(self.context, 0, ZString)
		self.infos = ArrayPointer(self.context, self.info_count, LayerFrag._import_path_map["generated.formats.matcol.compounds.Info"])
		self.attribs = ArrayPointer(self.context, self.attrib_count, LayerFrag._import_path_map["generated.formats.matcol.compounds.Attrib"])
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
		self.layer_name = Pointer(self.context, 0, ZString)
		self.infos = ArrayPointer(self.context, self.info_count, LayerFrag._import_path_map["generated.formats.matcol.compounds.Info"])
		self.attribs = ArrayPointer(self.context, self.attrib_count, LayerFrag._import_path_map["generated.formats.matcol.compounds.Attrib"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.layer_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.u_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.u_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.infos = ArrayPointer.from_stream(stream, instance.context, instance.info_count, LayerFrag._import_path_map["generated.formats.matcol.compounds.Info"])
		instance.info_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.u_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.u_3 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.attribs = ArrayPointer.from_stream(stream, instance.context, instance.attrib_count, LayerFrag._import_path_map["generated.formats.matcol.compounds.Attrib"])
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
		Uint64.to_stream(stream, instance.u_0)
		Uint64.to_stream(stream, instance.u_1)
		ArrayPointer.to_stream(stream, instance.infos)
		Uint64.to_stream(stream, instance.info_count)
		Uint64.to_stream(stream, instance.u_2)
		Uint64.to_stream(stream, instance.u_3)
		ArrayPointer.to_stream(stream, instance.attribs)
		Uint64.to_stream(stream, instance.attrib_count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'layer_name', Pointer, (0, ZString), (False, None)
		yield 'u_0', Uint64, (0, None), (False, None)
		yield 'u_1', Uint64, (0, None), (False, None)
		yield 'infos', ArrayPointer, (instance.info_count, LayerFrag._import_path_map["generated.formats.matcol.compounds.Info"]), (False, None)
		yield 'info_count', Uint64, (0, None), (False, None)
		yield 'u_2', Uint64, (0, None), (False, None)
		yield 'u_3', Uint64, (0, None), (False, None)
		yield 'attribs', ArrayPointer, (instance.attrib_count, LayerFrag._import_path_map["generated.formats.matcol.compounds.Attrib"]), (False, None)
		yield 'attrib_count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'LayerFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
