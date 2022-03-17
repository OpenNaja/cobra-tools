
from generated.io import MAX_LEN

ZERO = b"\x00"


from generated.context import ContextReference


class SmartPadding:

	"""
	Grabs 00 bytes only
	"""

	context = ContextReference()

	def set_defaults(self):
		pass

<<<<<<< HEAD
	def __init__(self, context, arg=0, template=None):
=======
	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
>>>>>>> 693ff8b... Finished finalizing generalized interface.
		self._context = context
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""

	def read(self, stream):
		self.read_fields(stream, self)

	def write(self, stream):
		self.write_fields(stream, fields)

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

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		cls.read_fields(stream, instance)
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		cls.write_fields(stream, instance)
		return instance

