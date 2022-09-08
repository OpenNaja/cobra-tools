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
