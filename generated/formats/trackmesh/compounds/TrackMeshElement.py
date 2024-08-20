from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackmesh.imports import name_type_map


class TrackMeshElement(MemStruct):

	"""
	PC: 120 bytes
	"""

	__name__ = 'TrackMesh_Element'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.objects_count = name_type_map['Uint64'](self.context, 0, None)
		self.flanges_count = name_type_map['Uint64'].from_value(1)
		self.start_1_count = name_type_map['Uint64'](self.context, 0, None)
		self.start_2_count = name_type_map['Uint64'](self.context, 0, None)
		self.f = name_type_map['Uint64'](self.context, 0, None)
		self.g = name_type_map['Uint64'](self.context, 0, None)
		self.stop_1_count = name_type_map['Uint64'](self.context, 0, None)
		self.stop_2_count = name_type_map['Uint64'](self.context, 0, None)
		self.element_id = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.objects_list = name_type_map['Pointer'](self.context, self.objects_count, name_type_map['ZStringList'])
		self.flanges = name_type_map['Pointer'](self.context, self.flanges_count, name_type_map['ZStringList'])
		self.start_1 = name_type_map['Pointer'](self.context, self.start_1_count, name_type_map['ZStringList'])
		self.start_2 = name_type_map['Pointer'](self.context, self.start_2_count, name_type_map['ZStringList'])
		self.stop_1 = name_type_map['Pointer'](self.context, self.stop_1_count, name_type_map['ZStringList'])
		self.stop_2 = name_type_map['Pointer'](self.context, self.stop_2_count, name_type_map['ZStringList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'element_id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'objects_list', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'objects_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'flanges', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'flanges_count', name_type_map['Uint64'], (0, None), (False, 1), (None, None)
		yield 'start_1', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'start_1_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'start_2', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'start_2_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'f', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'g', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'stop_1', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'stop_1_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'stop_2', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'stop_2_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'element_id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'objects_list', name_type_map['Pointer'], (instance.objects_count, name_type_map['ZStringList']), (False, None)
		yield 'objects_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'flanges', name_type_map['Pointer'], (instance.flanges_count, name_type_map['ZStringList']), (False, None)
		yield 'flanges_count', name_type_map['Uint64'], (0, None), (False, 1)
		yield 'start_1', name_type_map['Pointer'], (instance.start_1_count, name_type_map['ZStringList']), (False, None)
		yield 'start_1_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'start_2', name_type_map['Pointer'], (instance.start_2_count, name_type_map['ZStringList']), (False, None)
		yield 'start_2_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'f', name_type_map['Uint64'], (0, None), (False, None)
		yield 'g', name_type_map['Uint64'], (0, None), (False, None)
		yield 'stop_1', name_type_map['Pointer'], (instance.stop_1_count, name_type_map['ZStringList']), (False, None)
		yield 'stop_1_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'stop_2', name_type_map['Pointer'], (instance.stop_2_count, name_type_map['ZStringList']), (False, None)
		yield 'stop_2_count', name_type_map['Uint64'], (0, None), (False, None)
