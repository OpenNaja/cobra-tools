from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ForwardActivitySmoothTransitionData(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'ForwardActivitySmoothTransitionData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = name_type_map['Ubyte'](self.context, 0, None)
		self.unk_1 = name_type_map['Ubyte'](self.context, 0, None)
		self._padding_0 = name_type_map['Ushort'](self.context, 0, None)
		self._padding_1 = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unk_0', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'unk_1', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield '_padding_0', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield '_padding_1', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_0', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'unk_1', name_type_map['Ubyte'], (0, None), (False, None)
		yield '_padding_0', name_type_map['Ushort'], (0, None), (False, None)
		yield '_padding_1', name_type_map['Uint'], (0, None), (False, None)
