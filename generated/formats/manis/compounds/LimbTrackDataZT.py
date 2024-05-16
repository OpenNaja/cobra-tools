from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class LimbTrackDataZT(BaseStruct):

	__name__ = 'LimbTrackDataZT'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.limb_count = name_type_map['Uint64'](self.context, 0, None)
		self.pad = name_type_map['Uint64'](self.context, 0, None)
		self.limbs = Array(self.context, 0, None, (0,), name_type_map['LimbInfoZT'])
		self.limbs_data = name_type_map['LimbChunkReaderZt'](self.context, self.limbs, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'limb_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'pad', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'limbs', Array, (0, None, (None,), name_type_map['LimbInfoZT']), (False, None), (None, None)
		yield 'limbs_data', name_type_map['LimbChunkReaderZt'], (None, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'limb_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'pad', name_type_map['Uint64'], (0, None), (False, None)
		yield 'limbs', Array, (0, None, (instance.limb_count,), name_type_map['LimbInfoZT']), (False, None)
		yield 'limbs_data', name_type_map['LimbChunkReaderZt'], (instance.limbs, None), (False, None)
