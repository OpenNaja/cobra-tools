from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SinglePtr(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'SinglePtr'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptr = Pointer(self.context, 0, self.template)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ptr = Pointer(self.context, 0, self.template)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.ptr = Pointer.from_stream(stream, instance.context, 0, instance.template)
		if not isinstance(instance.ptr, int):
			instance.ptr.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.ptr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'ptr', Pointer, (0, instance.template), (False, None)

	def get_info_str(self, indent=0):
		return f'SinglePtr [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ptr = {self.fmt_member(self.ptr, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
