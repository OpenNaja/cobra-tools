from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PathSupport(MemStruct):

	__name__ = 'PathSupport'

	_import_key = 'path.compounds.PathSupport'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.distance = 10.0
		self._unk_int_1 = 0
		self.support = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('support', Pointer, (0, ZString), (False, None), None)
		yield ('distance', Float, (0, None), (False, 10.0), None)
		yield ('_unk_int_1', Uint, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'support', Pointer, (0, ZString), (False, None)
		yield 'distance', Float, (0, None), (False, 10.0)
		yield '_unk_int_1', Uint, (0, None), (False, None)


PathSupport.init_attributes()
