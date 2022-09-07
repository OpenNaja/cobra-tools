from generated.array import Array
from generated.formats.motiongraph.compounds.TransStruct import TransStruct
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TransStructArray(MemStruct):

	__name__ = 'TransStructArray'

	_import_path = 'generated.formats.motiongraph.compounds.TransStructArray'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.array = Array(self.context, 0, None, (0,), TransStruct)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.array = Array(self.context, 0, None, (self.arg,), TransStruct)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.array = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), TransStruct)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.array, instance.context, 0, None, (instance.arg,), TransStruct)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'array', Array, (0, None, (instance.arg,), TransStruct), (False, None)

	def get_info_str(self, indent=0):
		return f'TransStructArray [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
