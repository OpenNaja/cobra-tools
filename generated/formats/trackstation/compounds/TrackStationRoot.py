import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackStationRoot(MemStruct):

	"""
	PC and PZ: 128 bytes
	"""

	__name__ = 'TrackStationRoot'

	_import_key = 'trackstation.compounds.TrackStationRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_floats = Array(self.context, 0, None, (0,), Float)
		self.unk_ints = Array(self.context, 0, None, (0,), Uint)
		self.unk_ints_2 = Array(self.context, 0, None, (0,), Uint)
		self.unk_floats_2 = Array(self.context, 0, None, (0,), Float)
		self.unk_ints_3 = Array(self.context, 0, None, (0,), Uint)
		self.some_dataa = Pointer(self.context, 0, TrackStationRoot._import_map["trackstation.compounds.FirstPointersa"])
		self.some_datab = Pointer(self.context, 0, TrackStationRoot._import_map["trackstation.compounds.FirstPointersb"])
		self.stationpiece_name_0 = Pointer(self.context, 0, ZString)
		self.stationpiece_name_1 = Pointer(self.context, 0, ZString)
		self.stationpiece_name_2 = Pointer(self.context, 0, ZString)
		self.stationpiece_name_3 = Pointer(self.context, 0, ZString)
		self.stationpiece_name_4 = Pointer(self.context, 0, ZString)
		self.stationpiece_name_5 = Pointer(self.context, 0, ZString)
		self.stationpiece_name_6 = Pointer(self.context, 0, ZString)
		self.stationpiece_name_7 = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('unk_floats', Array, (0, None, (2,), Float), (False, None), None)
		yield ('unk_ints', Array, (0, None, (2,), Uint), (False, None), None)
		yield ('some_dataa', Pointer, (0, TrackStationRoot._import_map["trackstation.compounds.FirstPointersa"]), (False, None), None)
		yield ('some_datab', Pointer, (0, TrackStationRoot._import_map["trackstation.compounds.FirstPointersb"]), (False, None), None)
		yield ('stationpiece_name_0', Pointer, (0, ZString), (False, None), None)
		yield ('stationpiece_name_1', Pointer, (0, ZString), (False, None), None)
		yield ('stationpiece_name_2', Pointer, (0, ZString), (False, None), None)
		yield ('stationpiece_name_3', Pointer, (0, ZString), (False, None), None)
		yield ('stationpiece_name_4', Pointer, (0, ZString), (False, None), None)
		yield ('unk_ints_2', Array, (0, None, (2,), Uint), (False, None), None)
		yield ('stationpiece_name_5', Pointer, (0, ZString), (False, None), None)
		yield ('stationpiece_name_6', Pointer, (0, ZString), (False, None), None)
		yield ('stationpiece_name_7', Pointer, (0, ZString), (False, None), None)
		yield ('unk_floats_2', Array, (0, None, (4,), Float), (False, None), None)
		yield ('unk_ints_3', Array, (0, None, (2,), Uint), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_floats', Array, (0, None, (2,), Float), (False, None)
		yield 'unk_ints', Array, (0, None, (2,), Uint), (False, None)
		yield 'some_dataa', Pointer, (0, TrackStationRoot._import_map["trackstation.compounds.FirstPointersa"]), (False, None)
		yield 'some_datab', Pointer, (0, TrackStationRoot._import_map["trackstation.compounds.FirstPointersb"]), (False, None)
		yield 'stationpiece_name_0', Pointer, (0, ZString), (False, None)
		yield 'stationpiece_name_1', Pointer, (0, ZString), (False, None)
		yield 'stationpiece_name_2', Pointer, (0, ZString), (False, None)
		yield 'stationpiece_name_3', Pointer, (0, ZString), (False, None)
		yield 'stationpiece_name_4', Pointer, (0, ZString), (False, None)
		yield 'unk_ints_2', Array, (0, None, (2,), Uint), (False, None)
		yield 'stationpiece_name_5', Pointer, (0, ZString), (False, None)
		yield 'stationpiece_name_6', Pointer, (0, ZString), (False, None)
		yield 'stationpiece_name_7', Pointer, (0, ZString), (False, None)
		yield 'unk_floats_2', Array, (0, None, (4,), Float), (False, None)
		yield 'unk_ints_3', Array, (0, None, (2,), Uint), (False, None)


TrackStationRoot.init_attributes()
