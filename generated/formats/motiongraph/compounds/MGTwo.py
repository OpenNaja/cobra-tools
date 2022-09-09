from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MGTwo(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'MGTwo'

	_import_path = 'generated.formats.motiongraph.compounds.MGTwo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.ptr = Pointer(self.context, self.count, MGTwo._import_path_map["generated.formats.motiongraph.compounds.PtrList"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'ptr', Pointer, (instance.count, MGTwo._import_path_map["generated.formats.motiongraph.compounds.PtrList"]), (False, None)
