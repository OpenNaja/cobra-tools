from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class QuatWFirst(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.w = 1.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.w = 1.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.w = stream.read_float()
		instance.x = stream.read_float()
		instance.y = stream.read_float()
		instance.z = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.w)
		stream.write_float(instance.x)
		stream.write_float(instance.y)
		stream.write_float(instance.z)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield 'w', Float, (0, None)
		yield 'x', Float, (0, None)
		yield 'y', Float, (0, None)
		yield 'z', Float, (0, None)

	def __repr__(self):
		return f"[ {self.x:6.3f} {self.y:6.3f} {self.z:6.3f} {self.w:6.3f} ]"

