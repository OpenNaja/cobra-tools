# START_GLOBALS
from generated.base_struct import BaseStruct
from generated.io import MAX_LEN

ZERO = b"\x00"


# END_GLOBALS

class FloatsGrabber(BaseStruct):
	"""Holds a buffer of zero-terminated strings"""

# START_CLASS

	def __init__(self, context, arg=None, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = b""

	def __repr__(self, indent=0):
		return f"{self.data} Size: {len(self.data)}"

	@classmethod
	def read_fields(cls, stream, instance):
		instance.data = b''
		for i in range(MAX_LEN):
			end = stream.tell()
			f = stream.read(4)
			if len(f) != 4:
				raise ValueError('reached eof before finding 00 00 00 00')
			# stop if 4 00 bytes are found (if stream reaches eof it may not be 4 bytes so take len)
			if f == len(f) * ZERO:
				break
			# it's not 00 00 00 00 so add it
			instance.data += f
		else:
			raise ValueError('padding too long')
		stream.seek(end)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write(instance.data)

