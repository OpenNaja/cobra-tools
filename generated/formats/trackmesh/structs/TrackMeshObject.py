from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackmesh.imports import name_type_map


class TrackMeshObject(MemStruct):

	"""
	PC : 48 bytes
	PC2: 64 bytes
	"""

	__name__ = 'TrackMesh_Object'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.type = name_type_map['Uint'](self.context, 0, None)
		self.b = name_type_map['Uint'](self.context, 0, None)
		self.c = name_type_map['Uint'](self.context, 0, None)
		self.xtra_1 = name_type_map['Float'].from_value(1.0)
		self.xtra_2 = name_type_map['Uint64'](self.context, 0, None)
		self.e = name_type_map['Uint64'](self.context, 0, None)
		self.place_id = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.file = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.attachment_start = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.attachment_end = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'place_id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'file', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'type', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'c', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'xtra_1', name_type_map['Float'], (0, None), (False, 1.0), (None, None)
		yield 'xtra_2', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.is_pc_2, None)
		yield 'attachment_start', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'attachment_end', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'e', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.is_pc_2, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'place_id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'file', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'type', name_type_map['Uint'], (0, None), (False, None)
		yield 'b', name_type_map['Uint'], (0, None), (False, None)
		yield 'c', name_type_map['Uint'], (0, None), (False, None)
		yield 'xtra_1', name_type_map['Float'], (0, None), (False, 1.0)
		if instance.context.is_pc_2:
			yield 'xtra_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'attachment_start', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'attachment_end', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if instance.context.is_pc_2:
			yield 'e', name_type_map['Uint64'], (0, None), (False, None)
