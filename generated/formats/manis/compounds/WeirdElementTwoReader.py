import logging
import traceback

from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import get_padding_size, get_padding
from generated.formats.manis.compounds.ManiBlock import ManiBlock
from generated.formats.manis.compounds.WeirdElementTwo import WeirdElementTwo


from generated.base_struct import BaseStruct


class WeirdElementTwoReader(BaseStruct):

	__name__ = 'WeirdElementTwoReader'

	_import_key = 'manis.compounds.WeirdElementTwoReader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for chunk_sizes in instance.arg:
			chunk_sizes.keys = ()
		for elem_one in instance.arg:
			# print(mani_info)
			# print(stream.tell())
			elem_one.keys = Array.from_stream(stream, elem_one.context, arg=0, template=None, shape=(elem_one.countb,), dtype=WeirdElementTwo)
			# chunk_sizes.keys = WeirdElementTwo.from_stream(stream, instance.context, chunk_sizes, None)
			# print(elem_one)
			# print(elem_one.keys)
			# break
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for mani_info in instance.arg:
			ManiBlock.to_stream(mani_info.keys, stream, instance.context)
			for mb in mani_info.keys.repeats:
				stream.write(mb.data)
				stream.write(get_padding(mb.byte_size))
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for mani_info in instance.arg:
			s += str(mani_info.keys)
		return s


