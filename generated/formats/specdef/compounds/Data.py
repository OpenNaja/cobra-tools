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

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = ReferenceToObjectData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone
		# leaving self.dtype alone

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.arg == 0:
			instance.dtype = BooleanData.from_stream(stream, instance.context, 0, None)
		if instance.arg == 1:
			instance.dtype = Int8Data.from_stream(stream, instance.context, 0, None)
		if instance.arg == 2:
			instance.dtype = Int16Data.from_stream(stream, instance.context, 0, None)
		if instance.arg == 3:
			instance.dtype = Int32Data.from_stream(stream, instance.context, 0, None)
		if instance.arg == 4:
			instance.dtype = Int64Data.from_stream(stream, instance.context, 0, None)
		if instance.arg == 5:
			instance.dtype = Uint8Data.from_stream(stream, instance.context, 0, None)
		if instance.arg == 6:
			instance.dtype = Uint16Data.from_stream(stream, instance.context, 0, None)
		if instance.arg == 7:
			instance.dtype = Uint32Data.from_stream(stream, instance.context, 0, None)
		if instance.arg == 8:
			instance.dtype = Uint64Data.from_stream(stream, instance.context, 0, None)
		if instance.arg == 9:
			instance.dtype = FloatData.from_stream(stream, instance.context, 0, None)
		if instance.arg == 10:
			instance.dtype = StringData.from_stream(stream, instance.context, 0, None)
		if instance.arg == 11:
			instance.dtype = Vector2.from_stream(stream, instance.context, 0, None)
		if instance.arg == 12:
			instance.dtype = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.arg == 13:
			instance.dtype = ArrayData.from_stream(stream, instance.context, 0, None)
		if instance.arg == 14:
			instance.dtype = ChildSpecData.from_stream(stream, instance.context, 0, None)
		if instance.arg == 15:
			instance.dtype = ReferenceToObjectData.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.arg == 0:
			BooleanData.to_stream(stream, instance.dtype)
		if instance.arg == 1:
			Int8Data.to_stream(stream, instance.dtype)
		if instance.arg == 2:
			Int16Data.to_stream(stream, instance.dtype)
		if instance.arg == 3:
			Int32Data.to_stream(stream, instance.dtype)
		if instance.arg == 4:
			Int64Data.to_stream(stream, instance.dtype)
		if instance.arg == 5:
			Uint8Data.to_stream(stream, instance.dtype)
		if instance.arg == 6:
			Uint16Data.to_stream(stream, instance.dtype)
		if instance.arg == 7:
			Uint32Data.to_stream(stream, instance.dtype)
		if instance.arg == 8:
			Uint64Data.to_stream(stream, instance.dtype)
		if instance.arg == 9:
			FloatData.to_stream(stream, instance.dtype)
		if instance.arg == 10:
			StringData.to_stream(stream, instance.dtype)
		if instance.arg == 11:
			Vector2.to_stream(stream, instance.dtype)
		if instance.arg == 12:
			Vector3.to_stream(stream, instance.dtype)
		if instance.arg == 13:
			ArrayData.to_stream(stream, instance.dtype)
		if instance.arg == 14:
			ChildSpecData.to_stream(stream, instance.dtype)
		if instance.arg == 15:
			ReferenceToObjectData.to_stream(stream, instance.dtype)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
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

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* dtype = {self.fmt_member(self.dtype, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
