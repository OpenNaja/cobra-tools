from generated.formats.ms2.compounds.Capsule import Capsule
from generated.formats.ms2.imports import name_type_map


class Cylinder(Capsule):

	"""
	identical data to capsule, just imported differently
	"""

	__name__ = 'Cylinder'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# probably padding
		self.zeros_2 = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'zeros_2', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version == 32, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version == 32:
			yield 'zeros_2', name_type_map['Uint'], (0, None), (False, None)
