from generated.base_struct import BaseStruct
from generated.io import MAX_LEN

ZERO = b"\x00"


from generated.base_struct import BaseStruct


class FloatsGrabber(BaseStruct):

	__name__ = 'FloatsGrabber'


	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

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
			f = stream.read(24)
			if len(f) != 24:
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
