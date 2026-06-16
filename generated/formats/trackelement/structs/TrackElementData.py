from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackelement.imports import name_type_map


class TrackElementData(MemStruct):

	"""
	PC: was 80, now it is 72
	PZ: 48
	PC2: was 88, now it is 112
	"""

	__name__ = 'TrackElementData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.trackmeshlist_count = name_type_map['Uint'](self.context, 0, None)
		self.unk_count = name_type_map['Uint'](self.context, 0, None)
		self.direction = name_type_map['Uint'](self.context, 0, None)
		self.unk_2 = name_type_map['Uint'](self.context, 0, None)

		# Every bit encodes some track property
		self.tracktype_bitfield = name_type_map['TracktypeBitfield'].from_value(0)
		self.start_connection_bitfield = name_type_map['Uint'].from_value(1)
		self.end_connection_bitfield = name_type_map['Uint'].from_value(1)

		# Used to offset the track on the Y when there is no spline (e.g. double line segments)
		self.offset = name_type_map['Float'](self.context, 0, None)
		self.unk_5 = name_type_map['Uint'].from_value(0)

		# X offset
		self.x_offset = name_type_map['Float'].from_value(0)

		# Y offset
		self.y_offset = name_type_map['Float'].from_value(0)

		# Z offset
		self.z_offset = name_type_map['Float'].from_value(0)

		# Yaw offset
		self.yaw_offset = name_type_map['Float'].from_value(0)

		# Pitch offset
		self.pitch_offset = name_type_map['Float'].from_value(0)

		# Roll offset
		self.roll_offset = name_type_map['Float'].from_value(0)

		# Will require a _l_spline and _r_spline spl files
		self.spline_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.u_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.u_2 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])

		# This is a ref to an existing trackmesh element
		self.trackmesh_element_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])

		# Used for TrackMeshIndex params, points to trackmesh elements by name. PZ does not support this param in the fdb.
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
		yield 'tracktype_bitfield', name_type_map['TracktypeBitfield'], (0, None), (False, 0), (None, None)
		yield 'start_connection_bitfield', name_type_map['Uint'], (0, None), (False, 1), (None, None)
		yield 'end_connection_bitfield', name_type_map['Uint'], (0, None), (False, 1), (None, None)
		yield 'offset', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_5', name_type_map['Uint'], (0, None), (False, 0), (None, None)
		yield 'x_offset', name_type_map['Float'], (0, None), (False, 0), (lambda context: context.version >= 12, None)
		yield 'y_offset', name_type_map['Float'], (0, None), (False, 0), (lambda context: context.version >= 12, None)
		yield 'z_offset', name_type_map['Float'], (0, None), (False, 0), (lambda context: context.version >= 12, None)
		yield 'yaw_offset', name_type_map['Float'], (0, None), (False, 0), (lambda context: context.version >= 12, None)
		yield 'pitch_offset', name_type_map['Float'], (0, None), (False, 0), (lambda context: context.version >= 12, None)
		yield 'roll_offset', name_type_map['Float'], (0, None), (False, 0), (lambda context: context.version >= 12, None)

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
		yield 'tracktype_bitfield', name_type_map['TracktypeBitfield'], (0, None), (False, 0)
		yield 'start_connection_bitfield', name_type_map['Uint'], (0, None), (False, 1)
		yield 'end_connection_bitfield', name_type_map['Uint'], (0, None), (False, 1)
		yield 'offset', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_5', name_type_map['Uint'], (0, None), (False, 0)
		if instance.context.version >= 12:
			yield 'x_offset', name_type_map['Float'], (0, None), (False, 0)
			yield 'y_offset', name_type_map['Float'], (0, None), (False, 0)
			yield 'z_offset', name_type_map['Float'], (0, None), (False, 0)
			yield 'yaw_offset', name_type_map['Float'], (0, None), (False, 0)
			yield 'pitch_offset', name_type_map['Float'], (0, None), (False, 0)
			yield 'roll_offset', name_type_map['Float'], (0, None), (False, 0)
