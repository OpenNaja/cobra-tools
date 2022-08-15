from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class Vector4(BaseStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# zeroth coordinate.
		self.w = 0.0

		# First coordinate.
		self.x = 0.0

		# Second coordinate.
		self.y = 0.0

		# Third coordinate.
		self.z = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.w = 0.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.w = Float.from_stream(stream, instance.context, 0, None)
		instance.x = Float.from_stream(stream, instance.context, 0, None)
		instance.y = Float.from_stream(stream, instance.context, 0, None)
		instance.z = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.w)
		stream.write_float(instance.x)
		stream.write_float(instance.y)
		stream.write_float(instance.z)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'w', Float, (0, None)
		yield 'x', Float, (0, None)
		yield 'y', Float, (0, None)
		yield 'z', Float, (0, None)

	def get_info_str(self, indent=0):
		return f'Vector4 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* w = {self.fmt_member(self.w, indent+1)}'
		s += f'\n	* x = {self.fmt_member(self.x, indent+1)}'
		s += f'\n	* y = {self.fmt_member(self.y, indent+1)}'
		s += f'\n	* z = {self.fmt_member(self.z, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
