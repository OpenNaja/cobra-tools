from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackmesh.imports import name_type_map


class TrackMeshElement(MemStruct):

	"""
	PC : 120 bytes
	PC2: 128 bytes
	"""

	__name__ = 'TrackMesh_Element'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.objects_list_count = name_type_map['Uint64'](self.context, 0, None)
		self.flanges_count = name_type_map['Uint64'].from_value(1)
		self.start_1_count = name_type_map['Uint64'](self.context, 0, None)
		self.start_2_count = name_type_map['Uint64'](self.context, 0, None)
		self.start_3_count = name_type_map['Uint64'](self.context, 0, None)
		self.stop_1_count = name_type_map['Uint64'](self.context, 0, None)
		self.stop_2_count = name_type_map['Uint64'](self.context, 0, None)
		self.unknown_1 = name_type_map['Uint64'].from_value(0)
		self.element_id = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.objects_list = name_type_map['Pointer'](self.context, self.objects_list_count, name_type_map['ZStringList'])
		self.flanges = name_type_map['Pointer'](self.context, self.flanges_count, name_type_map['ZStringList'])
		self.start_1 = name_type_map['Pointer'](self.context, self.start_1_count, name_type_map['ZStringList'])
		self.start_2 = name_type_map['Pointer'](self.context, self.start_2_count, name_type_map['ZStringList'])
		self.start_3 = name_type_map['Pointer'](self.context, self.start_3_count, name_type_map['ZStringList'])
		self.stop_1 = name_type_map['Pointer'](self.context, self.stop_1_count, name_type_map['ZStringList'])
		self.stop_2 = name_type_map['Pointer'](self.context, self.stop_2_count, name_type_map['ZStringList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'element_id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'objects_list', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'objects_list_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'flanges', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'flanges_count', name_type_map['Uint64'], (0, None), (False, 1), (None, None)
		yield 'start_1', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'start_1_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'start_2', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'start_2_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'start_3', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'start_3_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'stop_1', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'stop_1_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'stop_2', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'stop_2_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unknown_1', name_type_map['Uint64'], (0, None), (False, 0), (lambda context: context.is_pc_2, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'element_id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'objects_list', name_type_map['Pointer'], (instance.objects_list_count, name_type_map['ZStringList']), (False, None)
		yield 'objects_list_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'flanges', name_type_map['Pointer'], (instance.flanges_count, name_type_map['ZStringList']), (False, None)
		yield 'flanges_count', name_type_map['Uint64'], (0, None), (False, 1)
		yield 'start_1', name_type_map['Pointer'], (instance.start_1_count, name_type_map['ZStringList']), (False, None)
		yield 'start_1_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'start_2', name_type_map['Pointer'], (instance.start_2_count, name_type_map['ZStringList']), (False, None)
		yield 'start_2_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'start_3', name_type_map['Pointer'], (instance.start_3_count, name_type_map['ZStringList']), (False, None)
		yield 'start_3_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'stop_1', name_type_map['Pointer'], (instance.stop_1_count, name_type_map['ZStringList']), (False, None)
		yield 'stop_1_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'stop_2', name_type_map['Pointer'], (instance.stop_2_count, name_type_map['ZStringList']), (False, None)
		yield 'stop_2_count', name_type_map['Uint64'], (0, None), (False, None)
		if instance.context.is_pc_2:
			yield 'unknown_1', name_type_map['Uint64'], (0, None), (False, 0)
