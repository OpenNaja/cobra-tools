from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.path.imports import name_type_map


class Footer(MemStruct):

	__name__ = 'Footer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.footer_model = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.ext_model = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.joint_model = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'footer_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'ext_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'joint_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_floats', Array, (0, None, (2,), name_type_map['Float']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'footer_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'ext_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'joint_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_floats', Array, (0, None, (2,), name_type_map['Float']), (False, None)
