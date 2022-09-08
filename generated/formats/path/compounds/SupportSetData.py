from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class SupportSetData(MemStruct):

	__name__ = 'SupportSetData'

	_import_path = 'generated.formats.path.compounds.SupportSetData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_index = 0
		self.unk_int_1 = 0
		self.unk_int_2 = 0
		self.unk_float_1 = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk_index = 0
		self.unk_int_1 = 0
		self.unk_int_2 = 0
		self.unk_float_1 = 0.0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_index', Uint, (0, None), (False, None)
		yield 'unk_int_1', Uint, (0, None), (False, None)
		yield 'unk_int_2', Uint, (0, None), (False, None)
		yield 'unk_float_1', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'SupportSetData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
