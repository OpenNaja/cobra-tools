from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.compounds.FloatInputData import FloatInputData
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class VariableBlendedAnimationActivityData(MemStruct):

	"""
	? bytes
	"""

	__name__ = 'VariableBlendedAnimationActivityData'

	_import_key = 'motiongraph.compounds.VariableBlendedAnimationActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.priorities = 0
		self._pad = 0
		self.weight = FloatInputData(self.context, 0, None)
		self.animation_count = 0
		self.variable_blended_animation_flags = 0
		self.animations = ArrayPointer(self.context, self.animation_count, VariableBlendedAnimationActivityData._import_map["motiongraph.compounds.VariableBlendedAnimationData"])
		self.variable = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('priorities', Uint, (0, None), (False, None), (None, None))
		yield ('_pad', Uint, (0, None), (False, None), (None, None))
		yield ('weight', FloatInputData, (0, None), (False, None), (None, None))
		yield ('animations', ArrayPointer, (None, VariableBlendedAnimationActivityData._import_map["motiongraph.compounds.VariableBlendedAnimationData"]), (False, None), (None, None))
		yield ('animation_count', Uint64, (0, None), (False, None), (None, None))
		yield ('variable', Pointer, (0, ZString), (False, None), (None, None))
		yield ('variable_blended_animation_flags', Uint, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'priorities', Uint, (0, None), (False, None)
		yield '_pad', Uint, (0, None), (False, None)
		yield 'weight', FloatInputData, (0, None), (False, None)
		yield 'animations', ArrayPointer, (instance.animation_count, VariableBlendedAnimationActivityData._import_map["motiongraph.compounds.VariableBlendedAnimationData"]), (False, None)
		yield 'animation_count', Uint64, (0, None), (False, None)
		yield 'variable', Pointer, (0, ZString), (False, None)
		yield 'variable_blended_animation_flags', Uint, (0, None), (False, None)
