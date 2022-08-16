from generated.formats.base.basic import Uint
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class GenericInfo(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# byte offset to name in fgm buffer
		self._name_offset = 0
		self.dtype = FgmDtype(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self._name_offset = 0
		# leaving self.dtype alone

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance._name_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.dtype = FgmDtype.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance._name_offset)
		FgmDtype.to_stream(stream, instance.dtype)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield '_name_offset', Uint, (0, None), (False, None)
		yield 'dtype', FgmDtype, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'GenericInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* _name_offset = {self.fmt_member(self._name_offset, indent+1)}'
		s += f'\n	* dtype = {self.fmt_member(self.dtype, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
