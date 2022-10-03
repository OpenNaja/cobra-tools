from generated.base_struct import BaseStruct


class FixedString(BaseStruct):

	"""
	The string "DDS ".
	"""

	__name__ = 'FixedString'

	_import_key = 'dds.compounds.FixedString'

	_attribute_list = BaseStruct._attribute_list + [
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def __init__(self, context, arg=0, template=None):
		self.name = ''
		self._context = context
		# arg is byte count
		self.arg = arg
		self.template = template
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
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template)
		cls.read_fields(stream, instance)
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		cls.write_fields(stream, instance)
		return instance
