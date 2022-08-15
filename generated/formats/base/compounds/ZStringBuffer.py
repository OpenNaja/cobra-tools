
from io import BytesIO
import logging

from generated.formats.base.basic import ZString
from modules.formats.shared import get_padding

ZERO = b"\x00"


from generated.base_struct import BaseStruct


class ZStringBuffer(BaseStruct):

	"""
	Holds a buffer of zero-terminated strings
	"""

	def set_defaults(self):
		super().set_defaults()
		pass

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)

	def __init__(self, context, arg=0, template=None):
		self.name = ''
		self._context = context
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""
		self.strings = []

	def get_str_at(self, pos):
		end = self.data.find(ZERO, pos)
		return self.data[pos:end].decode()

	def update_with(self, list_of_arrays):
		"""Updates this name buffer with a list of (array, attrib) whose elements have
		offset: bytes relative to the start of the name block
		[attrib]: string"""
		logging.debug("Updating name buffer")
		self.strings = []
		offset_dic = {}
		with BytesIO() as stream:

			for array, attrib in list_of_arrays:
				for item in sorted(array, key=lambda i: getattr(i, attrib)):
					name = getattr(item, attrib)
					if name in offset_dic:
						# known string, just get offset
						address = offset_dic[name]
					else:
						# new string, store offset and write zstring
						address = stream.tell()
						self.strings.append(name)
						offset_dic[name] = address
						ZString.to_stream(stream, name)
					# store offset on item
					item.offset = address
			# get the actual result buffer
			buffer_bytes = stream.getvalue()

		self.data = buffer_bytes + get_padding(len(buffer_bytes), alignment=8)

	def __repr__(self):
		return str(self.strings)

	@classmethod
	def read_fields(cls, stream, instance):
		instance.data = stream.read(instance.arg)
		instance.strings = instance.data.split(ZERO)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write(instance.data)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template)
		cls.read_fields(stream, instance)
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		cls.write_fields(stream, instance)
		return instance

