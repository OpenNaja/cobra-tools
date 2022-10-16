class FixedString:
	"""Holds a string of a fixed size, given as an argument."""

# START_CLASS

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = b""

	def __repr__(self):
		return str(self.data)

	@classmethod
	def read_fields(cls, stream, instance):
		instance.data = stream.read(instance.arg)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write(instance.data)

	@classmethod
	def validate_instance(cls, instance, context, arguments):
		super().validate_instance(instance, context, arguments)
		assert len(instance.data) == arguments[0]

	@staticmethod
	def get_size(instance, context):
		return len(instance.data)