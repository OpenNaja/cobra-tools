from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackmesh.imports import name_type_map


class TrackMeshOffset(MemStruct):

	"""
	-- Rename this to TrackMesh_Offset
	PC : 64 bytes
	PC2: 72 bytes
	"""

	__name__ = 'TrackMesh_Offset'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.relative_offset = name_type_map['Vector3'](self.context, 0, None)
		self.spacing = name_type_map['Float'](self.context, 0, None)
		self.one = name_type_map['Uint'](self.context, 0, None)
		self.min_pitch = name_type_map['Float'](self.context, 0, None)
		self.min_yaw = name_type_map['Float'](self.context, 0, None)
		self.flags = name_type_map['Uint'](self.context, 0, None)
		self.z_4 = name_type_map['Uint'](self.context, 0, None)
		self.z_5 = name_type_map['Uint'](self.context, 0, None)
		self.z_6 = name_type_map['Uint64'](self.context, 0, None)
		self.offset_id = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.mdl_2_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.bone_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'offset_id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'mdl_2_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'bone_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'relative_offset', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'spacing', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'one', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'min_pitch', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'min_yaw', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'z_4', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'z_5', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'z_6', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.is_pc_2, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset_id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'mdl_2_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'bone_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'relative_offset', name_type_map['Vector3'], (0, None), (False, None)
		yield 'spacing', name_type_map['Float'], (0, None), (False, None)
		yield 'one', name_type_map['Uint'], (0, None), (False, None)
		yield 'min_pitch', name_type_map['Float'], (0, None), (False, None)
		yield 'min_yaw', name_type_map['Float'], (0, None), (False, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None)
		yield 'z_4', name_type_map['Uint'], (0, None), (False, None)
		yield 'z_5', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.is_pc_2:
			yield 'z_6', name_type_map['Uint64'], (0, None), (False, None)
