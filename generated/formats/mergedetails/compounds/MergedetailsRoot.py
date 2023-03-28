from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MergedetailsRoot(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'MergedetailsRoot'

	_import_key = 'mergedetails.compounds.MergedetailsRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_0 = 0
		self.zero_1 = 0
		self.count = 0
		self.flag = 0
		self.merge_names = Pointer(self.context, self.count, MergedetailsRoot._import_map["mergedetails.compounds.PtrList"])
		self.queries = Pointer(self.context, self.count, MergedetailsRoot._import_map["mergedetails.compounds.PtrList"])
		self.field_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('merge_names', Pointer, (None, MergedetailsRoot._import_map["mergedetails.compounds.PtrList"]), (False, None), None)
		yield ('zero_0', Uint64, (0, None), (False, None), None)
		yield ('zero_1', Uint64, (0, None), (False, None), None)
		yield ('queries', Pointer, (None, MergedetailsRoot._import_map["mergedetails.compounds.PtrList"]), (False, None), None)
		yield ('field_name', Pointer, (0, ZString), (False, None), None)
		yield ('count', Uint, (0, None), (False, None), None)
		yield ('flag', Uint, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'merge_names', Pointer, (instance.count, MergedetailsRoot._import_map["mergedetails.compounds.PtrList"]), (False, None)
		yield 'zero_0', Uint64, (0, None), (False, None)
		yield 'zero_1', Uint64, (0, None), (False, None)
		yield 'queries', Pointer, (instance.count, MergedetailsRoot._import_map["mergedetails.compounds.PtrList"]), (False, None)
		yield 'field_name', Pointer, (0, ZString), (False, None)
		yield 'count', Uint, (0, None), (False, None)
		yield 'flag', Uint, (0, None), (False, None)


MergedetailsRoot.init_attributes()
