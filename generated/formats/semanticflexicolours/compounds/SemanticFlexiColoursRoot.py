from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class SemanticFlexiColoursRoot(MemStruct):

	__name__ = 'SemanticFlexiColoursRoot'

	_import_key = 'semanticflexicolours.compounds.SemanticFlexiColoursRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.name_count = 0
		self.name_list = ArrayPointer(self.context, self.name_count, SemanticFlexiColoursRoot._import_map["semanticflexicolours.compounds.Colourname"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('name_list', ArrayPointer, (None, SemanticFlexiColoursRoot._import_map["semanticflexicolours.compounds.Colourname"]), (False, None), (None, None))
		yield ('name_count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name_list', ArrayPointer, (instance.name_count, SemanticFlexiColoursRoot._import_map["semanticflexicolours.compounds.Colourname"]), (False, None)
		yield 'name_count', Uint64, (0, None), (False, None)
