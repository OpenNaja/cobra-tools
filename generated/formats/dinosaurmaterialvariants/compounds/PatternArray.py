from generated.array import Array
from generated.formats.dinosaurmaterialvariants.compounds.Pattern import Pattern
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PatternArray(MemStruct):

	__name__ = 'PatternArray'

	_import_path = 'generated.formats.dinosaurmaterialvariants.compounds.PatternArray'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.patterns = Array(self.context, 0, None, (0,), Pattern)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.patterns = Array(self.context, 0, None, (self.arg,), Pattern)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.patterns = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), Pattern)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.patterns, instance.context, 0, None, (instance.arg,), Pattern)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'patterns', Array, (0, None, (instance.arg,), Pattern), (False, None)

	def get_info_str(self, indent=0):
		return f'PatternArray [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
