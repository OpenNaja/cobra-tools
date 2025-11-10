import logging
from generated.base_struct import BaseStruct
from generated.formats.manis.structs.CompressedHeader import CompressedHeader

from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class CompressedHeaderReader(BaseStruct):

	__name__ = 'CompressedHeaderReader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'data', name_type_map['CompressedHeader'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if include_abstract:
			yield 'data', name_type_map['CompressedHeader'], (0, None), (False, None)

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		if cls.get_compressed_manis(instance):
			instance.data = CompressedHeader.from_stream(stream, instance.context)
		else:
			instance.data = None
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_compressed_manis(cls, instance):
		return [mani_info for mani_info in instance.arg if mani_info.dtype != 0]

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		if cls.get_compressed_manis(instance):
			CompressedHeader.to_stream(instance.data, stream, instance.context)
		instance.io_size = stream.tell() - instance.io_start


