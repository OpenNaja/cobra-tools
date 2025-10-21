from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class LimbTrackData(BaseStruct):

	__name__ = 'LimbTrackData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.padding_0 = name_type_map['SmartPadding'](self.context, 0, None)

		# 2 for bipeds, 4 for quadrupeds
		self.limb_count = name_type_map['Ushort'](self.context, 0, None)
		self.flag = name_type_map['Ushort'](self.context, 0, None)
		self.zero_1 = name_type_map['Uint'](self.context, 0, None)
		self.limbs = Array(self.context, self.arg, None, (0,), name_type_map['LimbInfo'])
		self.limbs_data = name_type_map['LimbChunkReader'](self.context, self.limbs, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'padding_0', name_type_map['SmartPadding'], (0, None), (False, None), (None, None)
		yield 'limb_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'flag', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zero_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'limbs', Array, (None, None, (None,), name_type_map['LimbInfo']), (False, None), (None, None)
		yield 'limbs_data', name_type_map['LimbChunkReader'], (None, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'padding_0', name_type_map['SmartPadding'], (0, None), (False, None)
		yield 'limb_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'flag', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zero_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'limbs', Array, (instance.arg, None, (instance.limb_count,), name_type_map['LimbInfo']), (False, None)
		yield 'limbs_data', name_type_map['LimbChunkReader'], (instance.limbs, None), (False, None)
