from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackelement.imports import name_type_map


class TrackElementData(MemStruct):

	"""
	PC: was 80, now it is 72
	PZ: 48
	PC2: 88
	"""

	__name__ = 'TrackElementData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.trackmeshlist_count = name_type_map['Uint'](self.context, 0, None)
		self.unk_count = name_type_map['Uint'](self.context, 0, None)
		self.direction = name_type_map['Uint'](self.context, 0, None)
		self.unk_2 = name_type_map['Uint'](self.context, 0, None)
		self.unk_3 = name_type_map['Ushort'].from_value(0)
		self.unk_4 = name_type_map['Ushort'].from_value(32)
		self.unk_5 = name_type_map['Uint'].from_value(1024)
		self.unk_6 = name_type_map['Uint'].from_value(1)
		self.unk_7 = name_type_map['Uint'].from_value(1)
		self.offset = name_type_map['Float'](self.context, 0, None)
		self.unk_9 = name_type_map['Uint'].from_value(0)
		self.spline_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.u_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.u_2 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.trackmesh_element_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.trackmeshlist = name_type_map['ArrayPointer'](self.context, self.trackmeshlist_count, name_type_map['TrackMeshRef'])
		self.optional_catwalk = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'spline_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'u_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: context.version >= 12, None)
		yield 'u_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: context.version >= 12, None)
		yield 'trackmesh_element_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'trackmeshlist', name_type_map['ArrayPointer'], (None, name_type_map['TrackMeshRef']), (False, None), (None, None)
		yield 'trackmeshlist_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'optional_catwalk', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'direction', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_3', name_type_map['Ushort'], (0, None), (False, 0), (None, None)
		yield 'unk_4', name_type_map['Ushort'], (0, None), (False, 32), (None, None)
		yield 'unk_5', name_type_map['Uint'], (0, None), (False, 1024), (None, None)
		yield 'unk_6', name_type_map['Uint'], (0, None), (False, 1), (None, None)
		yield 'unk_7', name_type_map['Uint'], (0, None), (False, 1), (None, None)
		yield 'offset', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_9', name_type_map['Uint'], (0, None), (False, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'spline_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if instance.context.version >= 12:
			yield 'u_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
			yield 'u_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'trackmesh_element_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'trackmeshlist', name_type_map['ArrayPointer'], (instance.trackmeshlist_count, name_type_map['TrackMeshRef']), (False, None)
		yield 'trackmeshlist_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'optional_catwalk', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'direction', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_3', name_type_map['Ushort'], (0, None), (False, 0)
		yield 'unk_4', name_type_map['Ushort'], (0, None), (False, 32)
		yield 'unk_5', name_type_map['Uint'], (0, None), (False, 1024)
		yield 'unk_6', name_type_map['Uint'], (0, None), (False, 1)
		yield 'unk_7', name_type_map['Uint'], (0, None), (False, 1)
		yield 'offset', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_9', name_type_map['Uint'], (0, None), (False, 0)
