from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PathSupport(MemStruct):

	__name__ = 'PathSupport'

	_import_path = 'generated.formats.path.compounds.PathSupport'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.distance = 10.0
		self._unk_int_1 = 0
		self.support = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.distance = 10.0
		self._unk_int_1 = 0
		self.support = Pointer(self.context, 0, ZString)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'support', Pointer, (0, ZString), (False, None)
		yield 'distance', Float, (0, None), (False, 10.0)
		yield '_unk_int_1', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'PathSupport [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
