import logging

from generated.formats.base.structs.PadAlign import get_padding_size, get_padding
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort, Ubyte
from generated.formats.manis.structs.ManiBlock import ManiBlock

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
		for mani_info, name in zip(instance.arg.mani_infos, instance.arg.names):
			# logging.info(mani_info)
			mani_info.name = name
			mani_block_start = stream.tell()
			logging.debug(f"Reading keys block at {mani_block_start}")
			bone_dtype = Ushort if mani_info.dtype.use_ushort else Ubyte
			try:
				cls.pad_to_start(instance, stream)
				mani_info.keys = ManiBlock.from_stream(stream, instance.context, mani_info, bone_dtype)
				# logging.info(mani_info)
				# logging.info(mani_info.keys)
				# break
			except:
				logging.exception(f"Reading ManiBlock failed at {mani_block_start} for {mani_info}")
				# raise
				break
		cls.pad_to_start(instance, stream)
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def pad_to_start(cls, instance, stream):
		pad_size = get_padding_size(stream.tell() - instance.io_start, alignment=16)
		# logging.info(f"padding {pad_size} bytes at {stream.tell()}")
		padding = stream.read(pad_size)
		if padding != b"\x00" * pad_size:
			logging.warning(f"Segment padding is not 00: '{padding}' at {stream.tell()}")

	@classmethod
	def align_to(cls, instance, stream, alignment=16, rel=None):
		abs_offset = stream.tell()
		relative_offset = abs_offset - instance.io_start
		padding_len = get_padding_size(relative_offset, alignment=alignment)
		# logging.debug(f"Aligning to {alignment} from {abs_offset} to {abs_offset+padding_len} ({padding_len} bytes)")
		stream.write(b'\x00' * padding_len)

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for mani_info in instance.arg.mani_infos:
			cls.align_to(instance, stream)
			ManiBlock.to_stream(mani_info.keys, stream, instance.context)
		cls.align_to(instance, stream)
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for mani_info in instance.arg.mani_infos:
			if hasattr(mani_info, "keys"):
				s += str(mani_info.keys)
		return s


