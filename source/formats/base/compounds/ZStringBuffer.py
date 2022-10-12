# START_GLOBALS
from io import BytesIO
import logging

from generated.formats.base.basic import ZString
from generated.formats.base.compounds.PadAlign import get_padding

ZERO = b"\x00"


# END_GLOBALS

class ZStringBuffer:
	"""Holds a buffer of zero-terminated strings, which can be accessed by their offset"""

# START_CLASS

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = b""
		self.strings = []
		self.offset_dic = {}

	def get_str_at(self, pos):
		end = self.data.find(ZERO, pos)
		return self.data[pos:end].decode()

	def update_with(self, list_of_arrays):
		"""Updates this name buffer with a list of (array, attrib) whose elements have
		offset: bytes relative to the start of the name block
		[attrib]: string"""
		logging.debug("Updating name buffer")
		self.strings = []
		self.offset_dic = {}
		with BytesIO() as stream:

			for array, attrib in list_of_arrays:
				for item in sorted(array, key=lambda i: getattr(i, attrib)):
					name = getattr(item, attrib)
					if name in self.offset_dic:
						# known string, just get offset
						address = self.offset_dic[name]
					else:
						# new string, store offset and write zstring
						address = stream.tell()
						self.strings.append(name)
						self.offset_dic[name] = address
						ZString.to_stream(name, stream, self.context)
					# store offset on item
					item.offset = address
			# get the actual result buffer
			buffer_bytes = stream.getvalue()
		self.data = buffer_bytes + get_padding(len(buffer_bytes), alignment=8)

	def update_strings(self, list_of_strs):
		"""Updates this name buffer with a list of names"""
		logging.debug("Updating name buffer")
		self.strings = sorted(set(list_of_strs))
		self.offset_dic = {}
		with BytesIO() as stream:
			for name in self.strings:
				# store offset and write zstring
				self.offset_dic[name] = stream.tell()
				ZString.to_stream(name, stream, self.context)
			# get the actual result buffer
			self.data = stream.getvalue()

	def __repr__(self):
		return str(self.strings)

	@classmethod
	def read_fields(cls, stream, instance):
		instance.data = stream.read(instance.arg)
		instance.strings = instance.data.split(ZERO)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write(instance.data)

