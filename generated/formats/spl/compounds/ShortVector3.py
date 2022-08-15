from generated.formats.base.basic import Short
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ShortVector3(MemStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# First coordinate.
		self.x = 0

		# Second coordinate.
		self.y = 0

		# Third coordinate.
		self.z = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.x = 0
		self.y = 0
		self.z = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.x = Short.from_stream(stream, instance.context, 0, None)
		instance.y = Short.from_stream(stream, instance.context, 0, None)
		instance.z = Short.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Short.to_stream(stream, instance.x)
		Short.to_stream(stream, instance.y)
		Short.to_stream(stream, instance.z)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'x', Short, (0, None)
		yield 'y', Short, (0, None)
		yield 'z', Short, (0, None)

	def get_info_str(self, indent=0):
		return f'ShortVector3 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* x = {self.fmt_member(self.x, indent+1)}'
		s += f'\n	* y = {self.fmt_member(self.y, indent+1)}'
		s += f'\n	* z = {self.fmt_member(self.z, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
