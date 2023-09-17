from generated.array import Array
from generated.formats.particleeffect.compounds.Effect import Effect
from generated.formats.particleeffect.imports import name_type_map


class Effect07(Effect):

	"""
	might map the different effects per emitter?
	144 bytes - PZ
	+ 16 bytes for JWE2
	"""

	__name__ = 'Effect07'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ints = Array(self.context, 0, None, (0,), name_type_map['Int'])
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.ints_2 = Array(self.context, 0, None, (0,), name_type_map['Int'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ints', Array, (0, None, (33,), name_type_map['Int']), (False, None), (None, None)
		yield 'floats', Array, (0, None, (4,), name_type_map['Float']), (False, None), (lambda context: context.version >= 37, None)
		yield 'ints_2', Array, (0, None, (3,), name_type_map['Int']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ints', Array, (0, None, (33,), name_type_map['Int']), (False, None)
		if instance.context.version >= 37:
			yield 'floats', Array, (0, None, (4,), name_type_map['Float']), (False, None)
		yield 'ints_2', Array, (0, None, (3,), name_type_map['Int']), (False, None)
