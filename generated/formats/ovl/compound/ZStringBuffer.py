
from generated.io import BinaryStream
from modules.formats.shared import get_padding

ZERO = b"\x00"


class ZStringBuffer:

	"""
	Holds a buffer of zero-terminated strings
	"""

	def __init__(self, arg=None, template=None):
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""
		self.strings = []

	def read(self, stream):
		self.data = stream.read(self.arg)
		self.strings = self.data.split(ZERO)

	def write(self, stream):
		stream.write(self.data)

	def get_str_at(self, pos):
		end = self.data.find(ZERO, pos)
		return self.data[pos:end].decode()

	def update_with(self, list_of_arrays):
		"""Updates this name buffer with a list of arrays whose elements have
		offset: bytes relative to the start of the name block
		name: string"""
		print("Updating name buffer")
		self.strings = []
		offset_dic = {}
		with BinaryStream() as stream:
			# for name in self.names:
			for array in list_of_arrays:
				for item in array:
					if item.name in offset_dic:
						# known string, just get offset
						address = offset_dic[item.name]
					else:
						# new string, store offset and write zstring
						address = stream.tell()
						self.strings.append(item.name)
						offset_dic[item.name] = address
						stream.write_zstring(item.name)
					# store offset on item
					item.offset = address
			# get the actual result buffer
			buffer_bytes = stream.getvalue()

		self.data = buffer_bytes + get_padding(len(buffer_bytes), alignment=8)

	def __repr__(self):
		return str(self.strings)

