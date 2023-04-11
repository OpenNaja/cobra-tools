from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import get_padding
from generated.formats.manis.compounds.ManiBlock import ManiBlock
from generated.formats.manis.compounds.UnkChunkList import UnkChunkList

from generated.base_struct import BaseStruct


class KeysReader(BaseStruct):

	__name__ = 'KeysReader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for mani_info in instance.arg:
			print(mani_info)
			print(stream.tell())
			if (mani_info.b >= 0) and (mani_info.b != 70) and (mani_info.count_a > 0) and (mani_info.count_b  > 0):
				mani_info.keys = ManiBlock.from_stream(stream, instance.context, mani_info, None)
				print(mani_info.keys)

				# sum_bytes = sum(mb.byte_size for mb in mani_info.keys.repeats)
				# print("sum_bytes", sum_bytes)
				# sum_bytes2 = sum(mb.byte_size + get_padding_size(mb.byte_size) for mb in mani_info.keys.repeats)
				# print("sum_bytes + padding", sum_bytes2)
				# for mb in mani_info.keys.repeats:
					# # print(bone_name, stream.tell())
					# mb.data = stream.read(mb.byte_size)
					# pad_size = get_padding_size(mb.byte_size)
					# mb.padding = stream.read(pad_size)
					# assert mb.padding == b"\x00" * pad_size
					# # print("end", stream.tell())
				# if (mani_info.keys.count > 0) and (mani_info.b > 5):
					# mani_info.subchunks = UnkChunkList.from_stream(stream, instance.context, mani_info, None)
					# print(mani_info.subchunks)
				# # break
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for mani_info in instance.arg:
			if (mani_info.b > 0) and (mani_info.b != 70) and (mani_info.count_a > 0) and (mani_info.count_b  > 0):
				ManiBlock.to_stream(mani_info.keys, stream, instance.context)
				for mb in mani_info.keys.repeats:
					stream.write(mb.data)
					stream.write(get_padding(mb.byte_size))
				if (mani_info.keys.count > 0) and (mani_info.b > 5):
					UnkChunkList.to_stream(mani_info.subchunks, stream, mani_info.subchunks.context)
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for mani_info in instance.arg:
			s += str(mani_info.keys)
		return s


