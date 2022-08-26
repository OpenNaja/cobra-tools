from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.specdef.compounds.Data import Data


class DataPtr(MemStruct):

	"""
	#ARG# is dtype
	"""

	__name__ = 'DataPtr'

	_import_path = 'generated.formats.specdef.compounds.DataPtr'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data_ptr = Pointer(self.context, self.arg.dtype, Data)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.data_ptr = Pointer(self.context, self.arg.dtype, Data)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.data_ptr = Pointer.from_stream(stream, instance.context, instance.arg.dtype, Data)
		if not isinstance(instance.data_ptr, int):
			instance.data_ptr.arg = instance.arg.dtype

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.data_ptr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'data_ptr', Pointer, (instance.arg.dtype, Data), (False, None)

	def get_info_str(self, indent=0):
		return f'DataPtr [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* data_ptr = {self.fmt_member(self.data_ptr, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
