from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte


class IKBlendType(BaseStruct):

	"""
	8 bytes
	"""

	__name__ = 'IKBlendType'

	_import_key = 'ms2.compounds.IKBlendType'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ik_blend_rearright = 0

		# last IK bone in the right leg
		self.ik_end_rearright = 0
		self.ik_blend_rearleft = 0
		self.ik_end_rearleft = 0
		self.ik_blend_frontright = 0

		# last IK bone in the right leg
		self.ik_end_frontright = 0
		self.ik_blend_frontleft = 0
		self.ik_end_frontleft = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('ik_blend_rearright', Ubyte, (0, None), (False, None), None),
		('ik_end_rearright', Ubyte, (0, None), (False, None), None),
		('ik_blend_rearleft', Ubyte, (0, None), (False, None), None),
		('ik_end_rearleft', Ubyte, (0, None), (False, None), None),
		('ik_blend_frontright', Ubyte, (0, None), (False, None), None),
		('ik_end_frontright', Ubyte, (0, None), (False, None), None),
		('ik_blend_frontleft', Ubyte, (0, None), (False, None), None),
		('ik_end_frontleft', Ubyte, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ik_blend_rearright', Ubyte, (0, None), (False, None)
		yield 'ik_end_rearright', Ubyte, (0, None), (False, None)
		yield 'ik_blend_rearleft', Ubyte, (0, None), (False, None)
		yield 'ik_end_rearleft', Ubyte, (0, None), (False, None)
		yield 'ik_blend_frontright', Ubyte, (0, None), (False, None)
		yield 'ik_end_frontright', Ubyte, (0, None), (False, None)
		yield 'ik_blend_frontleft', Ubyte, (0, None), (False, None)
		yield 'ik_end_frontleft', Ubyte, (0, None), (False, None)
