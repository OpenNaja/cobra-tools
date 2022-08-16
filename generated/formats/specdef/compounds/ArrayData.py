import generated.formats.specdef.compounds.Data
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.specdef.enums.SpecdefDtype import SpecdefDtype


class ArrayData(MemStruct):

	"""
	16 bytes in log
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = SpecdefDtype(self.context, 0, None)
		self.unused = 0
		self.item = Pointer(self.context, self.dtype, generated.formats.specdef.compounds.Data.Data)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		# leaving self.dtype alone
		self.unused = 0
		self.item = Pointer(self.context, self.dtype, generated.formats.specdef.compounds.Data.Data)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.item = Pointer.from_stream(stream, instance.context, instance.dtype, generated.formats.specdef.compounds.Data.Data)
		instance.dtype = SpecdefDtype.from_stream(stream, instance.context, 0, None)
		instance.unused = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.item, int):
			instance.item.arg = instance.dtype

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.item)
		SpecdefDtype.to_stream(stream, instance.dtype)
		Uint.to_stream(stream, instance.unused)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'item', Pointer, (instance.dtype, generated.formats.specdef.compounds.Data.Data), (False, None)
		yield 'dtype', SpecdefDtype, (0, None), (False, None)
		yield 'unused', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ArrayData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* item = {self.fmt_member(self.item, indent+1)}'
		s += f'\n	* dtype = {self.fmt_member(self.dtype, indent+1)}'
		s += f'\n	* unused = {self.fmt_member(self.unused, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
