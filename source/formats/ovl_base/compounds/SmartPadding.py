# START_GLOBALS
from generated.io import MAX_LEN

ZERO = b"\x00"


# END_GLOBALS

class SmartPadding:

# START_CLASS

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self.io_size = 0
		self.io_start = 0
		self._context = context
		# arg is size of the bytes raster
		self.arg = arg
		self.template = template
		self.data = b""

	@classmethod
	def format_indented(cls, self, indent=0):
		return f"{self.data} Size: {len(self.data)}"

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		instance.data = b''
		# fall back if no arg has been set
		if not instance.arg:
			raster = 1
		else:
			raster = instance.arg
		for i in range(MAX_LEN):
			end = stream.tell()
			chars = stream.read(raster)
			# stop if a byte other than 00 is encountered
			if chars != ZERO * raster:
				break
			# it's 00 so add it to the padding
			instance.data += chars
		else:
			raise ValueError('padding too long')
		stream.seek(end)
		instance.io_size = end - instance.io_start

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write(instance.data)

