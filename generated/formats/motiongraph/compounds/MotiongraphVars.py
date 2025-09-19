from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MotiongraphVars(MemStruct):

	__name__ = 'MotiongraphVars'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = name_type_map['Uint64'](self.context, 0, None)
		self.transition = name_type_map['Transition'](self.context, 0, None)
		self.ptr = name_type_map['ArrayPointer'](self.context, self.count, name_type_map['MotiongraphVar'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ptr', name_type_map['ArrayPointer'], (None, name_type_map['MotiongraphVar']), (False, None), (None, True)
		yield 'count', name_type_map['Uint64'], (0, None), (False, None), (None, True)
		yield 'transition', name_type_map['Transition'], (0, None), (False, None), (None, True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.arg == 7:
			yield 'ptr', name_type_map['ArrayPointer'], (instance.count, name_type_map['MotiongraphVar']), (False, None)
			yield 'count', name_type_map['Uint64'], (0, None), (False, None)
		if instance.arg == 8:
			yield 'transition', name_type_map['Transition'], (0, None), (False, None)
