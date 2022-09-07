from generated.formats.base.basic import Byte
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PathResource(MemStruct):

	__name__ = 'PathResource'

	_import_path = 'generated.formats.path.compounds.PathResource'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.path_type = 0
		self.path_sub_type = 0
		self.unk_byte_1 = 1
		self.unk_byte_2 = 0
		self.pathmaterial = Pointer(self.context, 0, ZString)
		self.pathextrusion_kerb = Pointer(self.context, 0, ZString)
		self.pathextrusion_railing = Pointer(self.context, 0, ZString)
		self.pathextrusion_ground = Pointer(self.context, 0, ZString)
		self.pathsupport = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.path_type = 0
		self.path_sub_type = 0
		self.unk_byte_1 = 1
		self.unk_byte_2 = 0
		self.pathmaterial = Pointer(self.context, 0, ZString)
		self.pathextrusion_kerb = Pointer(self.context, 0, ZString)
		self.pathextrusion_railing = Pointer(self.context, 0, ZString)
		self.pathextrusion_ground = Pointer(self.context, 0, ZString)
		self.pathsupport = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.pathmaterial = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.pathextrusion_kerb = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.pathextrusion_railing = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.pathextrusion_ground = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.pathsupport = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.path_type = Byte.from_stream(stream, instance.context, 0, None)
		instance.path_sub_type = Byte.from_stream(stream, instance.context, 0, None)
		instance.unk_byte_1 = Byte.from_stream(stream, instance.context, 0, None)
		instance.unk_byte_2 = Byte.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.pathmaterial, int):
			instance.pathmaterial.arg = 0
		if not isinstance(instance.pathextrusion_kerb, int):
			instance.pathextrusion_kerb.arg = 0
		if not isinstance(instance.pathextrusion_railing, int):
			instance.pathextrusion_railing.arg = 0
		if not isinstance(instance.pathextrusion_ground, int):
			instance.pathextrusion_ground.arg = 0
		if not isinstance(instance.pathsupport, int):
			instance.pathsupport.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.pathmaterial)
		Pointer.to_stream(stream, instance.pathextrusion_kerb)
		Pointer.to_stream(stream, instance.pathextrusion_railing)
		Pointer.to_stream(stream, instance.pathextrusion_ground)
		Pointer.to_stream(stream, instance.pathsupport)
		Byte.to_stream(stream, instance.path_type)
		Byte.to_stream(stream, instance.path_sub_type)
		Byte.to_stream(stream, instance.unk_byte_1)
		Byte.to_stream(stream, instance.unk_byte_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pathmaterial', Pointer, (0, ZString), (False, None)
		yield 'pathextrusion_kerb', Pointer, (0, ZString), (False, None)
		yield 'pathextrusion_railing', Pointer, (0, ZString), (False, None)
		yield 'pathextrusion_ground', Pointer, (0, ZString), (False, None)
		yield 'pathsupport', Pointer, (0, ZString), (False, None)
		yield 'path_type', Byte, (0, None), (False, None)
		yield 'path_sub_type', Byte, (0, None), (False, None)
		yield 'unk_byte_1', Byte, (0, None), (False, 1)
		yield 'unk_byte_2', Byte, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'PathResource [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
