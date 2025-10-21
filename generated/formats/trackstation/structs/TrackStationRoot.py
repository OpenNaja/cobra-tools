from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class TrackStationRoot(MemStruct):

	__name__ = 'TrackStationRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.station_grid_sizes = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.flags = name_type_map['Uint64'](self.context, 0, None)
		self.unknown_ptr = name_type_map['Uint64'].from_value(0)
		self.unknown_56 = name_type_map['Uint64'].from_value(0)
		self.unknown_72 = name_type_map['Uint64'].from_value(0)
		self.unk_ints_2 = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.unk_floats_2 = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.unk_floats_3 = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.corner_edge_track = name_type_map['Pointer'](self.context, 0, name_type_map['CornerEdgeTrack'])
		self.track_only = name_type_map['Pointer'](self.context, 0, name_type_map['CommonChunk'])
		self.control_box_front_panel = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.control_box_info = name_type_map['Pointer'](self.context, 0, name_type_map['ControlBoxInfo'])
		self.control_box_left_panel = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.gate_info = name_type_map['Pointer'](self.context, 0, name_type_map['GateInfo'])
		self.control_box_right_panel = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.entrance_gate = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.flume_info = name_type_map['Pointer'](self.context, 0, name_type_map['FlumeInfo'])
		self.exit_gate = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.fence_extrusion = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.small_fence_extrusion = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.fence_cap = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'station_grid_sizes', Array, (0, None, (2,), name_type_map['Float']), (False, None), (None, None)
		yield 'flags', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unknown_ptr', name_type_map['Uint64'], (0, None), (True, 0), (lambda context: context.is_pc_2, None)
		yield 'corner_edge_track', name_type_map['Pointer'], (0, name_type_map['CornerEdgeTrack']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'corner_edge_track', name_type_map['Pointer'], (0, name_type_map['CornerEdgeTrack']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'track_only', name_type_map['Pointer'], (0, name_type_map['CommonChunk']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'track_only', name_type_map['Pointer'], (0, name_type_map['CommonChunk']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'control_box_front_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'control_box_info', name_type_map['Pointer'], (0, name_type_map['ControlBoxInfo']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'control_box_left_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'gate_info', name_type_map['Pointer'], (0, name_type_map['GateInfo']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'control_box_right_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'unknown_56', name_type_map['Uint64'], (0, None), (True, 0), (lambda context: context.is_pc_2, None)
		yield 'entrance_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'flume_info', name_type_map['Pointer'], (0, name_type_map['FlumeInfo']), (False, None), (lambda context: context.is_pc_2, None)
		yield 'exit_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'unknown_72', name_type_map['Uint64'], (0, None), (True, 0), (lambda context: context.is_pc_2, None)
		yield 'unk_ints_2', Array, (0, None, (2,), name_type_map['Uint']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'fence_extrusion', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'small_fence_extrusion', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'fence_cap', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'unk_floats_2', Array, (0, None, (4,), name_type_map['Float']), (False, None), (lambda context: not context.is_pc_2, None)
		yield 'unk_floats_3', Array, (0, None, (2,), name_type_map['Uint']), (False, None), (lambda context: not context.is_pc_2, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'station_grid_sizes', Array, (0, None, (2,), name_type_map['Float']), (False, None)
		yield 'flags', name_type_map['Uint64'], (0, None), (False, None)
		if instance.context.is_pc_2:
			yield 'unknown_ptr', name_type_map['Uint64'], (0, None), (True, 0)
		if not instance.context.is_pc_2:
			yield 'corner_edge_track', name_type_map['Pointer'], (0, name_type_map['CornerEdgeTrack']), (False, None)
		if instance.context.is_pc_2:
			yield 'corner_edge_track', name_type_map['Pointer'], (0, name_type_map['CornerEdgeTrack']), (False, None)
		if not instance.context.is_pc_2:
			yield 'track_only', name_type_map['Pointer'], (0, name_type_map['CommonChunk']), (False, None)
		if instance.context.is_pc_2:
			yield 'track_only', name_type_map['Pointer'], (0, name_type_map['CommonChunk']), (False, None)
		if not instance.context.is_pc_2:
			yield 'control_box_front_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if instance.context.is_pc_2:
			yield 'control_box_info', name_type_map['Pointer'], (0, name_type_map['ControlBoxInfo']), (False, None)
		if not instance.context.is_pc_2:
			yield 'control_box_left_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if instance.context.is_pc_2:
			yield 'gate_info', name_type_map['Pointer'], (0, name_type_map['GateInfo']), (False, None)
		if not instance.context.is_pc_2:
			yield 'control_box_right_panel', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if instance.context.is_pc_2:
			yield 'unknown_56', name_type_map['Uint64'], (0, None), (True, 0)
		if not instance.context.is_pc_2:
			yield 'entrance_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if instance.context.is_pc_2:
			yield 'flume_info', name_type_map['Pointer'], (0, name_type_map['FlumeInfo']), (False, None)
		if not instance.context.is_pc_2:
			yield 'exit_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if instance.context.is_pc_2:
			yield 'unknown_72', name_type_map['Uint64'], (0, None), (True, 0)
		if not instance.context.is_pc_2:
			yield 'unk_ints_2', Array, (0, None, (2,), name_type_map['Uint']), (False, None)
			yield 'fence_extrusion', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
			yield 'small_fence_extrusion', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
			yield 'fence_cap', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
			yield 'unk_floats_2', Array, (0, None, (4,), name_type_map['Float']), (False, None)
			yield 'unk_floats_3', Array, (0, None, (2,), name_type_map['Uint']), (False, None)
