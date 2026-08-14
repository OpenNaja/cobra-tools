# START_GLOBALS
import logging
import struct

from generated.formats.base.structs.PadAlign import get_padding_size, get_padding
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort, Ubyte
from generated.formats.manis.structs.ManiBlock import ManiBlock

# END_GLOBALS


class KeysReader(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		instance.inter_block_data = []
		for block_i, (mani_info, name) in enumerate(zip(instance.arg.mani_infos, instance.arg.names)):
			mani_info.name = name
			bone_dtype = Ushort if mani_info.dtype.use_ushort else Ubyte
			try:
				if block_i == 0 or not cls.is_acl_manis(instance, mani_info):
					cls.pad_to_start(instance, stream)
					instance.inter_block_data.append(b"")
				else:
					gap_start = stream.tell()
					block_start = cls.find_acl_block_start(stream, instance, mani_info, bone_dtype)
					stream.seek(gap_start)
					instance.inter_block_data.append(stream.read(block_start - gap_start))
				mani_block_start = stream.tell()
				logging.debug(f"Reading keys block at {mani_block_start}")
				logging.info(mani_info)
				mani_info.keys = ManiBlock.from_stream(stream, instance.context, mani_info, bone_dtype)
				logging.info(mani_info.keys)
			except:
				logging.exception(f"Reading ManiBlock failed at {stream.tell()} for {mani_info}")
				break
		cls.pad_to_start(instance, stream)
		instance.io_size = stream.tell() - instance.io_start

	@staticmethod
	def is_acl_manis(instance, mani_info):
		return (
			instance.context.version == 262
			and instance.context.mani_version == 282
			and mani_info.dtype.compression > 0
		)

	@classmethod
	def find_acl_block_start(cls, stream, instance, mani_info, bone_dtype):
		"""Find a JWE3 ManiBlock after the preceding clip's auxiliary data."""
		origin = stream.tell()
		data = stream.read()
		stream.seek(origin)
		name_count = (
			mani_info.pos_bone_count
			+ mani_info.ori_bone_count
			+ mani_info.scl_bone_count
			+ mani_info.float_count
		)
		map_count = mani_info.pos_bone_count + mani_info.ori_bone_count + mani_info.scl_bone_count
		name_limit = len(instance.context.name_buffer.target_names)
		map_size = 2 if bone_dtype is Ushort else 1
		needed = name_count * 4 + map_count * map_size
		first_rel = get_padding_size(origin - instance.io_start, alignment=16)
		for rel in range(first_rel, len(data) - needed + 1, 16):
			name_values = struct.unpack_from(f"<{name_count}I", data, rel) if name_count else ()
			if name_values and (max(name_values) >= name_limit or len(set(name_values)) < 2):
				continue
			map_offset = rel + name_count * 4
			map_code = "H" if map_size == 2 else "B"
			map_values = struct.unpack_from(f"<{map_count}{map_code}", data, map_offset) if map_count else ()
			if map_values and (
				max(map_values) >= mani_info.target_bone_count
				or len(set(map_values)) < 2
			):
				continue
			return origin + rel
		raise BufferError(f"Could not find JWE3 ManiBlock for {mani_info.name} after {origin}")

	@classmethod
	def pad_to_start(cls, instance, stream):
		pad_size = get_padding_size(stream.tell() - instance.io_start, alignment=16)
		padding = stream.read(pad_size)
		if padding != b"\x00" * pad_size:
			logging.warning(f"Segment padding is not 00: '{padding}' at {stream.tell()}")

	@classmethod
	def align_to(cls, instance, stream, alignment=16, rel=None):
		abs_offset = stream.tell()
		relative_offset = abs_offset - instance.io_start
		padding_len = get_padding_size(relative_offset, alignment=alignment)
		stream.write(b'\x00' * padding_len)

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		gaps = getattr(instance, "inter_block_data", ())
		for block_i, mani_info in enumerate(instance.arg.mani_infos):
			if block_i and block_i < len(gaps) and gaps[block_i]:
				stream.write(gaps[block_i])
			else:
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
