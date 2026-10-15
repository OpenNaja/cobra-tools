# START_GLOBALS
import base64
import binascii

import numpy as np

from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
# END_GLOBALS


class Base64ArrayPointer(ArrayPointer):

	"""Keep the binary byte array; encode only its XML representation."""

	# START_CLASS

	@staticmethod
	def _byte_dtype(instance):
		dtype = np.dtype(instance.template.np_dtype)
		if dtype.itemsize != 1 or dtype.kind not in ("i", "u"):
			raise TypeError("Base64ArrayPointer requires a one-byte integer template")
		return dtype

	@staticmethod
	def _check_size(data, expected):
		if len(data) != expected:
			raise ValueError(
				f"file_content has {len(data)} decoded bytes; file_size is {expected}"
			)

	@classmethod
	def _to_xml(cls, instance, elem, debug):
		dtype = cls._byte_dtype(instance)
		if isinstance(instance.data, (bytes, bytearray, memoryview)):
			data = bytes(instance.data)
		else:
			data = np.asarray(instance.data, dtype=dtype).tobytes()
		cls._check_size(data, instance.arg)
		elem.set("encoding", "base64")
		elem.text = base64.b64encode(data).decode("ascii")

	@classmethod
	def _from_xml(cls, instance, elem):
		dtype = cls._byte_dtype(instance)
		# ArrayPointer.from_xml passes () when the element is missing.
		if not hasattr(elem, "get"):
			if instance.arg:
				raise ValueError("Missing file_content for non-empty file")
			instance.data = np.empty(0, dtype=dtype)
			return instance
		if len(elem):
			raise ValueError("file_content must contain text, not child elements")

		encoding = elem.get("encoding")
		text = elem.text or ""
		if encoding == "base64":
			try:
				# Accept indented or line-wrapped Base64, but reject bad input.
				data = base64.b64decode("".join(text.split()), validate=True)
			except (binascii.Error, ValueError) as exc:
				raise ValueError(f"Invalid Base64 file_content: {exc}") from exc
		elif encoding in (None, "decimal"):
			# Legacy exports contain signed Char values or unsigned byte values.
			try:
				values = [int(value, 10) for value in text.split()]
			except ValueError as exc:
				raise ValueError("Invalid decimal file_content") from exc
			if any(value < -128 or value > 255 for value in values):
				raise ValueError("Decimal file_content values must be between -128 and 255")
			data = bytes(value & 0xFF for value in values)
		else:
			raise ValueError(f"Unsupported file_content encoding: {encoding!r}")

		cls._check_size(data, instance.arg)
		# Retain Char's signed dtype: bytes >= 128 must keep their bit patterns.
		instance.data = np.frombuffer(data, dtype=dtype).copy()
		return instance
