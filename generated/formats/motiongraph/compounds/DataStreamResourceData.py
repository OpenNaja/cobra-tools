from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.compounds.CurveData import CurveData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DataStreamResourceData(MemStruct):

	"""
	56 bytes
	"""

	__name__ = 'DataStreamResourceData'

	_import_key = 'motiongraph.compounds.DataStreamResourceData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.curve_type = 0
		self.curve = CurveData(self.context, 0, None)
		self.ds_name = Pointer(self.context, 0, ZString)
		self.type = Pointer(self.context, 0, ZString)
		self.bone_i_d = Pointer(self.context, 0, ZString)
		self.location = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('curve_type', Uint64, (0, None), (False, None), None),
		('ds_name', Pointer, (0, ZString), (False, None), None),
		('type', Pointer, (0, ZString), (False, None), None),
		('bone_i_d', Pointer, (0, ZString), (False, None), None),
		('location', Pointer, (0, ZString), (False, None), None),
		('curve', CurveData, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'curve_type', Uint64, (0, None), (False, None)
		yield 'ds_name', Pointer, (0, ZString), (False, None)
		yield 'type', Pointer, (0, ZString), (False, None)
		yield 'bone_i_d', Pointer, (0, ZString), (False, None)
		yield 'location', Pointer, (0, ZString), (False, None)
		yield 'curve', CurveData, (0, None), (False, None)
