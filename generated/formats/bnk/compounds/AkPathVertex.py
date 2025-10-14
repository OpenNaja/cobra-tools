from generated.formats.bnk.compounds.Vec import Vec
from generated.formats.bnk.imports import name_type_map


class AkPathVertex(Vec):

	__name__ = 'AkPathVertex'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.duration = name_type_map['Int'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'duration', name_type_map['Int'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'duration', name_type_map['Int'], (0, None), (False, None)
