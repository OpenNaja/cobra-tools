from generated.formats.base.basic import Int
from generated.formats.voxelskirt.compounds.Material import Material


class PosInfo(Material):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# -1
		self.ff = 0

		# -1, 0 for PC
		self.ff_or_zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ff = 0
		self.ff_or_zero = 0

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
		instance.ff = stream.read_int()
		instance.ff_or_zero = stream.read_int()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_int(instance.ff)
		stream.write_int(instance.ff_or_zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'ff', Int, (0, None)
		yield 'ff_or_zero', Int, (0, None)

	def get_info_str(self, indent=0):
		return f'PosInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ff = {self.fmt_member(self.ff, indent+1)}'
		s += f'\n	* ff_or_zero = {self.fmt_member(self.ff_or_zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
