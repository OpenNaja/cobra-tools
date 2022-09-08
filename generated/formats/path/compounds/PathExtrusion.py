from generated.formats.base.basic import Float
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.basic import Bool
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PathExtrusion(MemStruct):

	__name__ = 'PathExtrusion'

	_import_path = 'generated.formats.path.compounds.PathExtrusion'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_float_1 = 0.0
		self.unk_float_2 = 0.0
		self.is_kerb = False
		self.is_not_ground = True
		self.model = Pointer(self.context, 0, ZString)
		self.post_model = Pointer(self.context, 0, ZString)
		self.endcap_model = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk_float_1 = 0.0
		self.unk_float_2 = 0.0
		self.is_kerb = False
		self.is_not_ground = True
		self.model = Pointer(self.context, 0, ZString)
		self.post_model = Pointer(self.context, 0, ZString)
		self.endcap_model = Pointer(self.context, 0, ZString)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'model', Pointer, (0, ZString), (False, None)
		yield 'post_model', Pointer, (0, ZString), (False, None)
		yield 'endcap_model', Pointer, (0, ZString), (False, None)
		yield 'unk_float_1', Float, (0, None), (False, None)
		yield 'unk_float_2', Float, (0, None), (False, None)
		yield 'is_kerb', Bool, (0, None), (False, None)
		yield 'is_not_ground', Bool, (0, None), (False, True)

	def get_info_str(self, indent=0):
		return f'PathExtrusion [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
