from generated.formats.motiongraphvars.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class MotiongraphVarsRoot(MemStruct):

	__name__ = 'MotiongraphVarsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.vars_count = name_type_map['Uint64'](self.context, 0, None)
		self.vars = name_type_map['Pointer'](self.context, self.vars_count, name_type_map['MotiongraphVars'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'vars_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'vars', name_type_map['ArrayPointer'], (None, name_type_map['MotiongraphVar']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'vars', name_type_map['Pointer'], (None, name_type_map['MotiongraphVars']), (False, None), (lambda context: context.is_pc_2, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'vars_count', name_type_map['Uint64'], (0, None), (False, None)
		if not instance.context.is_pc_2:
			yield 'vars', name_type_map['ArrayPointer'], (instance.vars_count, name_type_map['MotiongraphVar']), (False, None)
		if instance.context.is_pc_2:
			yield 'vars', name_type_map['Pointer'], (instance.vars_count, name_type_map['MotiongraphVars']), (False, None)
