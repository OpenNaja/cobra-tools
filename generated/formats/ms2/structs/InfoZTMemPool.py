from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.imports import name_type_map


class InfoZTMemPool(BaseStruct):

	__name__ = 'InfoZTMemPool'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ?
		self.unk_count = name_type_map['Ushort'](self.context, 0, None)

		# ?
		self.unks = Array(self.context, 0, None, (0,), name_type_map['Ushort'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unk_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unks', Array, (0, None, (None, 2,), name_type_map['Ushort']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unks', Array, (0, None, (instance.unk_count, 2,), name_type_map['Ushort']), (False, None)
