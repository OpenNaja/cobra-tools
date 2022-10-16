from generated.base_struct import BaseStruct


class FixedString(BaseStruct):

	"""
	Holds a string of a fixed size, given as #ARG#.
	"""

	__name__ = 'FixedString'

	_import_key = 'base.compounds.FixedString'

	_attribute_list = BaseStruct._attribute_list + [
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

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
