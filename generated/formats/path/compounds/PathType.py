from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PathType(MemStruct):

	__name__ = 'PathType'

	_import_path = 'generated.formats.path.compounds.PathType'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.enum_value = 0
		self.min_width = 4.0
		self.max_width = 10.0
		self._unk_int_2 = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'enum_value', Uint, (0, None), (False, None)
		yield 'min_width', Float, (0, None), (False, 4.0)
		yield 'max_width', Float, (0, None), (False, 10.0)
		yield '_unk_int_2', Uint, (0, None), (False, None)
