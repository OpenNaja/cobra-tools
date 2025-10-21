from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class Buffer1(BaseStruct):

	"""
	the game verifies that hash and target name match
	if they don't, the target won't be animated
	"""

	__name__ = 'Buffer1'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.target_hashes = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.target_names = Array(self.context, 0, None, (0,), name_type_map['ZString'])
		self.bone_pad = name_type_map['PadAlign'](self.context, 4, self.target_names)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'target_hashes', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'target_names', Array, (0, None, (None,), name_type_map['ZString']), (False, None), (None, None)
		yield 'bone_pad', name_type_map['PadAlign'], (4, None), (False, None), (lambda context: context.version >= 260, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'target_hashes', Array, (0, None, (instance.arg,), name_type_map['Uint']), (False, None)
		yield 'target_names', Array, (0, None, (instance.arg,), name_type_map['ZString']), (False, None)
		if instance.context.version >= 260:
			yield 'bone_pad', name_type_map['PadAlign'], (4, instance.target_names), (False, None)
