from io import BytesIO
import logging

from generated.formats.base.basic import ZString
from generated.formats.base.compounds.PadAlign import get_padding

ZERO = b"\x00"


from generated.base_struct import BaseStruct


class ZStringBuffer(BaseStruct):

	"""
	Holds a buffer of zero-terminated strings
	"""

	__name__ = 'ZStringBuffer'


	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = b""
		self.strings = []
		self.offset_dic = {}
		self.offset_2_str = {}

	def get_str_at(self, pos):
		try:
			return self.offset_2_str.get(pos)
		except:
			return self._get_str_at(pos)

	def _get_str_at(self, pos):
		end = self.data.find(ZERO, pos)
		s = self.data[pos:end].decode()
		logging.warning(f"Zstring '{s}' starts at {pos} in the middle of a Zstring")
		return s

	def update_strings(self, list_of_strs):
		"""Updates this name buffer with a list of names"""
		logging.debug("Updating name buffer")
		self.strings = sorted(set(list_of_strs))
		self.offset_dic = {}
		self.offset_2_str = {}
		with BytesIO() as stream:
			for name in self.strings:
				# store offset and write zstring
				self.offset_dic[name] = stream.tell()
				self.offset_2_str[stream.tell()] = name
				ZString.to_stream(name, stream, self.context)
			# get the actual result buffer
			buffer_bytes = stream.getvalue()
		self.data = buffer_bytes + get_padding(len(buffer_bytes), alignment=8)

	@classmethod
	def format_indented(cls, self, indent=0):
		return str(self.strings)

	@classmethod
	def read_fields(cls, stream, instance):
		instance.data = stream.read(instance.arg)
		instance.strings = instance.data.split(ZERO)
		instance.offset_2_str = {}
		offset = 0
		for s in instance.strings:
			instance.offset_2_str[offset] = s.decode()
			offset += len(s) + 1
		print(instance.offset_2_str)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write(instance.data)

	@staticmethod
	def validate_instance(instance, context, arg,  template):
		super().validate_instance(instance, context, arg, template)
		assert len(instance.data) == instance.arg

	@classmethod
	def get_size(cls, instance, context, arg=0, template=None):
		return len(instance.data)

