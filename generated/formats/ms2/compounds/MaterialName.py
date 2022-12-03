from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort


class MaterialName(BaseStruct):

	__name__ = 'MaterialName'

	_import_key = 'ms2.compounds.MaterialName'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into ms2 names array
		self.name_index = 0

		# specifies the blend mode, highly consistent to shader type used
		# PZ: 263: {'furshell', 'furpatchworkbaldnessshell', 'furpatchworkshell'}, 6: {'furpatchworkbaldnessfin', 'furfin', 'furpatchworkfin'}, 8: {'animal_whisker'}, 15: {'glass_textured_weather'}
		# JWE2: 7: {'dinosaurfur_vanilla_shell'}, 6: {'dinosaurfur_vanilla_fin'}
		self.blend_mode = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('name_index', Ushort, (0, None), (False, None), True),
		('name_index', Uint, (0, None), (False, None), True),
		('blend_mode', Ushort, (0, None), (False, None), True),
		('blend_mode', Uint, (0, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 32:
			yield 'name_index', Ushort, (0, None), (False, None)
		if instance.context.version >= 47:
			yield 'name_index', Uint, (0, None), (False, None)
		if instance.context.version <= 32:
			yield 'blend_mode', Ushort, (0, None), (False, None)
		if instance.context.version >= 47:
			yield 'blend_mode', Uint, (0, None), (False, None)
