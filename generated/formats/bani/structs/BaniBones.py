from generated.array import Array
from generated.formats.bani.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class BaniBones(MemStruct):

	"""
	PC2: multiples of 32 bytes for each bani, data per bone index
	"""

	__name__ = 'BaniBones'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.data = Array(self.context, 0, None, (0,), name_type_map['BoneInfo'])
		self.padding = name_type_map['PadAlign'](self.context, 32, self.ref)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'data', Array, (0, None, (None,), name_type_map['BoneInfo']), (False, None), (None, None)
		yield 'padding', name_type_map['PadAlign'], (32, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'data', Array, (0, None, (instance.arg.num_bones,), name_type_map['BoneInfo']), (False, None)
		yield 'padding', name_type_map['PadAlign'], (32, instance.ref), (False, None)
