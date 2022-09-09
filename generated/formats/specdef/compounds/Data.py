from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.specdef.compounds.ArrayData import ArrayData
from generated.formats.specdef.compounds.BooleanData import BooleanData
from generated.formats.specdef.compounds.ChildSpecData import ChildSpecData
from generated.formats.specdef.compounds.FloatData import FloatData
from generated.formats.specdef.compounds.Int16Data import Int16Data
from generated.formats.specdef.compounds.Int32Data import Int32Data
from generated.formats.specdef.compounds.Int64Data import Int64Data
from generated.formats.specdef.compounds.Int8Data import Int8Data
from generated.formats.specdef.compounds.ReferenceToObjectData import ReferenceToObjectData
from generated.formats.specdef.compounds.StringData import StringData
from generated.formats.specdef.compounds.Uint16Data import Uint16Data
from generated.formats.specdef.compounds.Uint32Data import Uint32Data
from generated.formats.specdef.compounds.Uint64Data import Uint64Data
from generated.formats.specdef.compounds.Uint8Data import Uint8Data
from generated.formats.specdef.compounds.Vector2 import Vector2
from generated.formats.specdef.compounds.Vector3 import Vector3


class Data(MemStruct):

	"""
	#ARG# is dtype
	todo - enum, grab, implement, fetch
	"""

	__name__ = 'Data'

	_import_path = 'generated.formats.specdef.compounds.Data'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = ReferenceToObjectData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.arg == 0:
			yield 'dtype', BooleanData, (0, None), (False, None)
		if instance.arg == 1:
			yield 'dtype', Int8Data, (0, None), (False, None)
		if instance.arg == 2:
			yield 'dtype', Int16Data, (0, None), (False, None)
		if instance.arg == 3:
			yield 'dtype', Int32Data, (0, None), (False, None)
		if instance.arg == 4:
			yield 'dtype', Int64Data, (0, None), (False, None)
		if instance.arg == 5:
			yield 'dtype', Uint8Data, (0, None), (False, None)
		if instance.arg == 6:
			yield 'dtype', Uint16Data, (0, None), (False, None)
		if instance.arg == 7:
			yield 'dtype', Uint32Data, (0, None), (False, None)
		if instance.arg == 8:
			yield 'dtype', Uint64Data, (0, None), (False, None)
		if instance.arg == 9:
			yield 'dtype', FloatData, (0, None), (False, None)
		if instance.arg == 10:
			yield 'dtype', StringData, (0, None), (False, None)
		if instance.arg == 11:
			yield 'dtype', Vector2, (0, None), (False, None)
		if instance.arg == 12:
			yield 'dtype', Vector3, (0, None), (False, None)
		if instance.arg == 13:
			yield 'dtype', ArrayData, (0, None), (False, None)
		if instance.arg == 14:
			yield 'dtype', ChildSpecData, (0, None), (False, None)
		if instance.arg == 15:
			yield 'dtype', ReferenceToObjectData, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Data [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
