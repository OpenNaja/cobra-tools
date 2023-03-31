from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FRenderContextSetRoot(MemStruct):

	__name__ = 'FRenderContextSetRoot'

	_import_key = 'frendercontextset.compounds.FRenderContextSetRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptr_1_count = 0
		self.ptr_2_count = 0
		self.ptr_3_count = 0
		self.ptr_1_list = ArrayPointer(self.context, self.ptr_1_count, FRenderContextSetRoot._import_map["frendercontextset.compounds.ContextSet1Item"])
		self.ptr_2_list = ArrayPointer(self.context, self.ptr_2_count, FRenderContextSetRoot._import_map["frendercontextset.compounds.ContextSet2Item"])
		self.ptr_3_list = ArrayPointer(self.context, self.ptr_3_count, FRenderContextSetRoot._import_map["frendercontextset.compounds.ContextSet3Item"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('ptr_1_list', ArrayPointer, (None, FRenderContextSetRoot._import_map["frendercontextset.compounds.ContextSet1Item"]), (False, None), (None, None))
		yield ('ptr_1_count', Uint64, (0, None), (False, None), (None, None))
		yield ('ptr_2_list', ArrayPointer, (None, FRenderContextSetRoot._import_map["frendercontextset.compounds.ContextSet2Item"]), (False, None), (None, None))
		yield ('ptr_2_count', Uint64, (0, None), (False, None), (None, None))
		yield ('ptr_3_list', ArrayPointer, (None, FRenderContextSetRoot._import_map["frendercontextset.compounds.ContextSet3Item"]), (False, None), (None, None))
		yield ('ptr_3_count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptr_1_list', ArrayPointer, (instance.ptr_1_count, FRenderContextSetRoot._import_map["frendercontextset.compounds.ContextSet1Item"]), (False, None)
		yield 'ptr_1_count', Uint64, (0, None), (False, None)
		yield 'ptr_2_list', ArrayPointer, (instance.ptr_2_count, FRenderContextSetRoot._import_map["frendercontextset.compounds.ContextSet2Item"]), (False, None)
		yield 'ptr_2_count', Uint64, (0, None), (False, None)
		yield 'ptr_3_list', ArrayPointer, (instance.ptr_3_count, FRenderContextSetRoot._import_map["frendercontextset.compounds.ContextSet3Item"]), (False, None)
		yield 'ptr_3_count', Uint64, (0, None), (False, None)


FRenderContextSetRoot.init_attributes()
