import logging
import struct

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
				logging.debug(mani_info)
				mani_info.keys = ManiBlock.from_stream(stream, instance.context, mani_info, bone_dtype)
				logging.debug(mani_info.keys)
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

	ACL_TRACKS_TAG = 0xAC11AC11
	ACL_TRANSFORM_TRACK_TYPE = 12

	@classmethod
	def acl_blob_offsets(cls, stream, instance):
		"""Offsets of every ACL transform blob in the keys buffer, relative to io_start.

		ACL's compressed_tracks tag is documented magic, so this is ground truth - unlike
		scanning for something that merely looks like a name table. Cached per instance
		because the whole buffer is read to build it.
		"""
		cached = getattr(instance, "_acl_blob_offsets", None)
		if cached is not None:
			return cached
		here = stream.tell()
		stream.seek(instance.io_start)
		data = stream.read()
		stream.seek(here)
		tag = struct.pack("<I", cls.ACL_TRACKS_TAG)
		offsets = []
		pos = 0
		while True:
			magic = data.find(tag, pos)
			if magic == -1:
				break
			start = magic - 8
			if start < 0:
				pos = magic + 1
				continue
			size = struct.unpack_from("<I", data, start)[0]
			if size < 32 or start + size > len(data):
				pos = magic + 1
				continue
			if data[start + 15] == cls.ACL_TRANSFORM_TRACK_TYPE:
				offsets.append(start)
			pos = start + size
		instance._acl_blob_offsets = offsets
		return offsets

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
		# Bound the search by this clip's ACL transform blob. The names and channel maps
		# sit immediately before it, so the block cannot start after it - and searching
		# BACKWARDS from there means the offset closest to the blob wins, instead of the
		# first stretch of auxiliary limb data that happens to look like a name table.
		origin_rel = origin - instance.io_start
		blob_rel = None
		for candidate in cls.acl_blob_offsets(stream, instance):
			if candidate >= origin_rel:
				blob_rel = candidate
				break
		search = range(first_rel, len(data) - needed + 1, 16)
		if blob_rel is not None:
			# `rel` is an offset into `data`, which starts at `origin`; blob_rel is
			# relative to io_start. Convert, then take the highest 16-aligned offset in
			# first_rel's residue class at or before the blob.
			blob_in_data = blob_rel - origin_rel
			last_rel = first_rel + (blob_in_data - first_rel) // 16 * 16
			last_rel = min(last_rel, len(data) - needed)
			if last_rel >= first_rel:
				search = range(last_rel, first_rel - 1, -16)
		for rel in search:
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

