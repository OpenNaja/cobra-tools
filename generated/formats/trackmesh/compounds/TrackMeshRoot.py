from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackMeshRoot(MemStruct):

	"""
	PC: 80 bytes
	"""

	__name__ = 'TrackMeshRoot'

	_import_key = 'trackmesh.compounds.TrackMeshRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = 0
		self.count_0 = 0
		self.next_count = 0
		self.last_count = 0
		self.lod_count = 0
		self.g = 0
		self.offset_data = ArrayPointer(self.context, self.count_0, TrackMeshRoot._import_map["trackmesh.compounds.OffsetData"])
		self.track_data = ArrayPointer(self.context, self.next_count, TrackMeshRoot._import_map["trackmesh.compounds.TrackData"])
		self.last = ArrayPointer(self.context, self.last_count, TrackMeshRoot._import_map["trackmesh.compounds.LastData"])
		self.lods = ArrayPointer(self.context, self.lod_count, TrackMeshRoot._import_map["trackmesh.compounds.Lod"])
		self.heatmap_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('a', Uint64, (0, None), (False, None), None)
		yield ('offset_data', ArrayPointer, (None, None), (False, None), None)
		yield ('track_data', ArrayPointer, (None, None), (False, None), None)
		yield ('last', ArrayPointer, (None, None), (False, None), None)
		yield ('count_0', Uint, (0, None), (False, None), None)
		yield ('next_count', Uint, (0, None), (False, None), None)
		yield ('last_count', Uint64, (0, None), (False, None), None)
		yield ('lods', ArrayPointer, (None, None), (False, None), None)
		yield ('lod_count', Uint64, (0, None), (False, None), None)
		yield ('heatmap_name', Pointer, (0, ZString), (False, None), None)
		yield ('g', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', Uint64, (0, None), (False, None)
		yield 'offset_data', ArrayPointer, (instance.count_0, TrackMeshRoot._import_map["trackmesh.compounds.OffsetData"]), (False, None)
		yield 'track_data', ArrayPointer, (instance.next_count, TrackMeshRoot._import_map["trackmesh.compounds.TrackData"]), (False, None)
		yield 'last', ArrayPointer, (instance.last_count, TrackMeshRoot._import_map["trackmesh.compounds.LastData"]), (False, None)
		yield 'count_0', Uint, (0, None), (False, None)
		yield 'next_count', Uint, (0, None), (False, None)
		yield 'last_count', Uint64, (0, None), (False, None)
		yield 'lods', ArrayPointer, (instance.lod_count, TrackMeshRoot._import_map["trackmesh.compounds.Lod"]), (False, None)
		yield 'lod_count', Uint64, (0, None), (False, None)
		yield 'heatmap_name', Pointer, (0, ZString), (False, None)
		yield 'g', Uint64, (0, None), (False, None)


TrackMeshRoot.init_attributes()
