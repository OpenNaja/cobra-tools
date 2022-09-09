from generated.array import Array
from generated.formats.dinosaurmaterialvariants.compounds.Pattern import Pattern
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PatternArray(MemStruct):

	__name__ = 'PatternArray'

	_import_key = 'dinosaurmaterialvariants.compounds.PatternArray'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.patterns = Array(self.context, 0, None, (0,), Pattern)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'patterns', Array, (0, None, (instance.arg,), Pattern), (False, None)
