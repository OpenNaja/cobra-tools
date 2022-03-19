from io import BytesIO
from struct import Struct
from contextlib import contextmanager
from typing import *


MAX_LEN = 1000


Byte = Struct("<b")  # int8
UByte = Struct("<B")  # uint8
Short = Struct("<h")  # int16
UShort = Struct("<H")  # uint16
Int = Struct("<i")  # int32
UInt = Struct("<I")  # uint32
Int64 = Struct("<q")  # int64
UInt64 = Struct("<Q")  # uint64
Float = Struct("<f")  # float32
HFloat = Struct("<e")  # float16


class BinaryStream(BytesIO):

	def __init__(self, initial_bytes=None):
		super().__init__(initial_bytes)

	def register_basic_functions(self, basic_map):
		for basic_name, basic_class in basic_map.items():
			if callable(getattr(basic_class, 'functions_for_stream')):
				l_basic_name = basic_name.lower()
				from_stream, to_stream, from_stream_array, to_stream_array = basic_class.functions_for_stream(self)
				setattr(self, f'read_{l_basic_name}', from_stream)
				setattr(self, f'write_{l_basic_name}', to_stream)
				setattr(self, f'read_{l_basic_name}s', from_stream_array)
				setattr(self, f'write_{l_basic_name}s', to_stream_array)


class IoFile:

	basic_map = None

	def load(self, filepath):
		with self.reader(filepath) as stream:
			self.read(stream)
			return stream.tell()

	def save(self, filepath):
		with self.writer(filepath) as stream:
			self.write(stream)
			return stream.tell()

	@classmethod
	@contextmanager
	def reader(cls, filepath) -> Generator[BinaryStream, None, None]:
		with open(filepath, "rb") as f:
			data = f.read()
		with BinaryStream(data) as stream:
			if cls.basic_map is not None:
				stream.register_basic_functions(cls.basic_map)
			yield stream  # type: ignore

	@classmethod
	@contextmanager
	def writer(cls, filepath) -> Generator[BinaryStream, None, None]:
		with BinaryStream() as stream:
			if cls.basic_map is not None:
				stream.register_basic_functions(cls.basic_map)
			yield stream  # type: ignore
			with open(filepath, "wb") as f:
				# noinspection PyTypeChecker
				f.write(stream.getbuffer())
