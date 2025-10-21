from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackmesh.imports import name_type_map


class TrackMeshRoot(MemStruct):

	"""
	PC: 80 bytes
	"""

	__name__ = 'TrackMeshRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = name_type_map['Uint64'](self.context, 0, None)
		self.offset_data_count = name_type_map['Uint'](self.context, 0, None)
		self.object_data_count = name_type_map['Uint'](self.context, 0, None)
		self.element_data_count = name_type_map['Uint64'](self.context, 0, None)
		self.lods_count = name_type_map['Uint64'](self.context, 0, None)
		self.g = name_type_map['Uint64'](self.context, 0, None)
		self.offset_data = name_type_map['ArrayPointer'](self.context, self.offset_data_count, name_type_map['TrackMeshOffset'])
		self.object_data = name_type_map['ArrayPointer'](self.context, self.object_data_count, name_type_map['TrackMeshObject'])
		self.element_data = name_type_map['ArrayPointer'](self.context, self.element_data_count, name_type_map['TrackMeshElement'])
		self.lods = name_type_map['ArrayPointer'](self.context, self.lods_count, name_type_map['Lod'])
		self.heatmap_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'a', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'offset_data', name_type_map['ArrayPointer'], (None, name_type_map['TrackMeshOffset']), (False, None), (None, None)
		yield 'object_data', name_type_map['ArrayPointer'], (None, name_type_map['TrackMeshObject']), (False, None), (None, None)
		yield 'element_data', name_type_map['ArrayPointer'], (None, name_type_map['TrackMeshElement']), (False, None), (None, None)
		yield 'offset_data_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'object_data_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'element_data_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'lods', name_type_map['ArrayPointer'], (None, name_type_map['Lod']), (False, None), (None, None)
		yield 'lods_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'heatmap_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'g', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', name_type_map['Uint64'], (0, None), (False, None)
		yield 'offset_data', name_type_map['ArrayPointer'], (instance.offset_data_count, name_type_map['TrackMeshOffset']), (False, None)
		yield 'object_data', name_type_map['ArrayPointer'], (instance.object_data_count, name_type_map['TrackMeshObject']), (False, None)
		yield 'element_data', name_type_map['ArrayPointer'], (instance.element_data_count, name_type_map['TrackMeshElement']), (False, None)
		yield 'offset_data_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'object_data_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'element_data_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'lods', name_type_map['ArrayPointer'], (instance.lods_count, name_type_map['Lod']), (False, None)
		yield 'lods_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'heatmap_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'g', name_type_map['Uint64'], (0, None), (False, None)
