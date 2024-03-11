from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class TrackStationRoot(MemStruct):

	"""
	PC and PZ: 128 bytes
	"""

	__name__ = 'TrackStationRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.unk_ints = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.unk_ints_2 = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.unk_floats_2 = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.unk_ints_3 = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.corner_edge_track = name_type_map['Pointer'](self.context, 0, name_type_map['CornerEdgeTrack'])
		self.track_only = name_type_map['Pointer'](self.context, 0, name_type_map['TrackOnly'])
		self.control_box_front_panel = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.control_box_left_panel = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.control_box_right_panel = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.entrance_gate = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.exit_gate = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.fence_ext = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.small_fence_ext = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.fence_cap = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unk_floats', Array, (0, None, (2,), name_type_map['Float']), (False, None), (None, None)
		yield 'unk_ints', Array, (0, None, (2,), name_type_map['Uint']), (False, None), (None, None)
		yield 'corner_edge_track', name_type_map['Pointer'], (0, name_type_map['CornerEdgeTrack']), (False, None), (None, None)
		yield 'track_only', name_type_map['Pointer'], (0, name_type_map['TrackOnly']), (False, None), (None, None)
		yield 'control_box_front_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'control_box_left_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'control_box_right_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'entrance_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'exit_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_ints_2', Array, (0, None, (2,), name_type_map['Uint']), (False, None), (None, None)
		yield 'fence_ext', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'small_fence_ext', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'fence_cap', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_floats_2', Array, (0, None, (4,), name_type_map['Float']), (False, None), (None, None)
		yield 'unk_ints_3', Array, (0, None, (2,), name_type_map['Uint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_floats', Array, (0, None, (2,), name_type_map['Float']), (False, None)
		yield 'unk_ints', Array, (0, None, (2,), name_type_map['Uint']), (False, None)
		yield 'corner_edge_track', name_type_map['Pointer'], (0, name_type_map['CornerEdgeTrack']), (False, None)
		yield 'track_only', name_type_map['Pointer'], (0, name_type_map['TrackOnly']), (False, None)
		yield 'control_box_front_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'control_box_left_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'control_box_right_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'entrance_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'exit_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_ints_2', Array, (0, None, (2,), name_type_map['Uint']), (False, None)
		yield 'fence_ext', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'small_fence_ext', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'fence_cap', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_floats_2', Array, (0, None, (4,), name_type_map['Float']), (False, None)
		yield 'unk_ints_3', Array, (0, None, (2,), name_type_map['Uint']), (False, None)
