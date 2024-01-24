from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class LimbChunk(BaseStruct):

	"""
	arg is LimbInfo
	"""

	__name__ = 'LimbChunk'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# for LimbChunk_list[n] needs limbs[n]'s counta for array length
		self.list_one = Array(self.context, 0, None, (0,), name_type_map['WeirdElementOne'])

		# needs sum of countb's from weird list one
		self.list_two = name_type_map['WeirdElementTwoReader'](self.context, self.list_one, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'list_one', Array, (0, None, (None,), name_type_map['WeirdElementOne']), (False, None), (None, None)
		yield 'list_two', name_type_map['WeirdElementTwoReader'], (None, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'list_one', Array, (0, None, (instance.arg.counta,), name_type_map['WeirdElementOne']), (False, None)
		yield 'list_two', name_type_map['WeirdElementTwoReader'], (instance.list_one, None), (False, None)
