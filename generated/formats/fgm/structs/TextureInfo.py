from generated.array import Array
from generated.formats.fgm.imports import name_type_map
from generated.formats.fgm.structs.GenericInfo import GenericInfo


class TextureInfo(GenericInfo):

	"""
	# PC2 - 16 bytes
	part of fgm fragment, per texture involved
	"""

	__name__ = 'TextureInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Stores 2 rgba colors

		# Stores rgba color
		self.value = Array(self.context, 0, None, (0,), name_type_map['ByteColor'])
		self.some_index_0 = name_type_map['Uint'].from_value(0)
		self.some_index_1 = name_type_map['Uint'].from_value(0)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'value', Array, (0, None, (1,), name_type_map['TexIndex']), (False, None), (None, True)
		yield 'value', Array, (0, None, (2,), name_type_map['ByteColor']), (False, None), (lambda context: context.version >= 18, True)
		yield 'value', Array, (0, None, (1,), name_type_map['ByteColor']), (False, None), (lambda context: context.version <= 17, True)
		yield 'some_index_0', name_type_map['Uint'], (0, None), (True, 0), (lambda context: context.version >= 18 and context.mime_version != 7, None)
		yield 'some_index_1', name_type_map['Uint'], (0, None), (True, 0), (lambda context: context.version >= 18 and context.mime_version != 7, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.dtype == 8:
			yield 'value', Array, (0, None, (1,), name_type_map['TexIndex']), (False, None)
		if instance.context.version >= 18 and instance.dtype == 7:
			yield 'value', Array, (0, None, (2,), name_type_map['ByteColor']), (False, None)
		if instance.context.version <= 17 and instance.dtype == 7:
			yield 'value', Array, (0, None, (1,), name_type_map['ByteColor']), (False, None)
		if instance.context.version >= 18 and instance.context.mime_version != 7:
			yield 'some_index_0', name_type_map['Uint'], (0, None), (True, 0)
			yield 'some_index_1', name_type_map['Uint'], (0, None), (True, 0)
