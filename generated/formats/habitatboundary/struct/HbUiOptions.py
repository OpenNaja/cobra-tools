from generated.formats.ovl_base.basic import Bool
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class HbUiOptions(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Controls the Straight-Curved option for barriers
		self.straight_curve = 0

		# Controls the Windows option for barriers
		self.windows = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.straight_curve = False
		self.windows = False

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
		instance.straight_curve = stream.read_bool()
		instance.windows = stream.read_bool()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_bool(instance.straight_curve)
		stream.write_bool(instance.windows)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('straight_curve', Bool, (0, None))
		yield ('windows', Bool, (0, None))

	def get_info_str(self, indent=0):
		return f'HbUiOptions [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* straight_curve = {self.fmt_member(self.straight_curve, indent+1)}'
		s += f'\n	* windows = {self.fmt_member(self.windows, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
