
from generated.io import MAX_LEN

ZERO = b"\x00"


from generated.base_struct import BaseStruct


class SmartPadding(BaseStruct):

	"""
	Grabs 00 bytes only
	"""

	def set_defaults(self):
		super().set_defaults()
		pass

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""

	def __repr__(self):
		return f"{self.data} Size: {len(self.data)}"

	@classmethod
	def read_fields(cls, stream, instance):
		instance.data = b''
		for i in range(MAX_LEN):
			end = stream.tell()
			char = stream.read(1)
			# stop if a byte other than 00 is encountered
			if char != ZERO:
				break
			# it's 00 so add it to the padding
			instance.data += char
		else:
			raise ValueError('padding too long')
		stream.seek(end)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write(instance.data)


