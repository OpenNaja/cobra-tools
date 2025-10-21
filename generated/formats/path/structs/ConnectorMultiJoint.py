from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.path.imports import name_type_map


class ConnectorMultiJoint(MemStruct):

	__name__ = 'ConnectorMultiJoint'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_joints = name_type_map['Uint'](self.context, 0, None)
		self.extent_min = name_type_map['Float'](self.context, 0, None)
		self.extent_max = name_type_map['Float'](self.context, 0, None)
		self.some_index = name_type_map['Uint'](self.context, 0, None)
		self.connector_model = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.support_model = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.joints = name_type_map['ArrayPointer'](self.context, self.num_joints, name_type_map['Joint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'connector_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'support_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'joints', name_type_map['ArrayPointer'], (None, name_type_map['Joint']), (False, None), (None, None)
		yield 'num_joints', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'extent_min', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'extent_max', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'some_index', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'connector_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'support_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'joints', name_type_map['ArrayPointer'], (instance.num_joints, name_type_map['Joint']), (False, None)
		yield 'num_joints', name_type_map['Uint'], (0, None), (False, None)
		yield 'extent_min', name_type_map['Float'], (0, None), (False, None)
		yield 'extent_max', name_type_map['Float'], (0, None), (False, None)
		yield 'some_index', name_type_map['Uint'], (0, None), (False, None)
