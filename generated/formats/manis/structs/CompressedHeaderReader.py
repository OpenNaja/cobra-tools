import logging
import struct

from generated.base_struct import BaseStruct

# ACL's compressed_database serialization tag
ACL_DATABASE_TAG = 0xAC11DB01
# raw_buffer_header is uint32 size + uint32 hash, then the tag
ACL_DATABASE_MIN_SIZE = 32

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
		"""Read the ACL compressed_database that sits between the ManiInfo array and
		the name buffer, if this bundle has one.

		JWE3 clips are ACL database-stripped: the retained frames live in the clip and
		the per-frame detail in database bulk blocks shipped as paired LOD streams. The
		database's own header sits here, at the tail of buffer 0, immediately after
		`mani_count * sizeof(ManiInfo)` bytes.

		This used to be modelled as a `CompressedHeader` struct of pointers, gated on
		`dtype.has_list == 3`. That was a guess which only ever worked because it
		happened to consume the same number of bytes, and it made the database
		mandatory: a bundle with the database removed failed to parse at all, because
		the reader consumed the name buffer in its place and then ran off the end of
		the file. It also mis-fired on the dtype 48/49 bundle, which has has_list == 1
		yet still carries a database.

		Detect the blob by ACL's tag and take it verbatim instead. Being byte-preserving
		matters as much here as it does in MANI.py: re-serialising a JWE3 manis through
		a guessed schema is what silently dropped this blob before.
		"""
		instance.io_start = stream.tell()
		instance.data = None
		head = stream.read(12)
		stream.seek(instance.io_start)
		if len(head) == 12:
			size, _hash, tag = struct.unpack("<III", head)
			if tag == ACL_DATABASE_TAG and size >= ACL_DATABASE_MIN_SIZE:
				instance.data = stream.read(size)
				if len(instance.data) != size:
					raise BufferError(
						f"ACL compressed_database claims {size} bytes but only "
						f"{len(instance.data)} were available")
		logging.debug(f"CompressedHeaderReader read {0 if instance.data is None else len(instance.data)} bytes")
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		if instance.data:
			stream.write(instance.data)
		instance.io_size = stream.tell() - instance.io_start
