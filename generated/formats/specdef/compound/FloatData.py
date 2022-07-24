from source.formats.base.basic import fmt_member
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class FloatData(MemStruct):

	"""
	16 bytes in log
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.imin = 0
		self.imax = 0
		self.ivalue = 0
		self.ioptional = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.imin = 0.0
		self.imax = 0.0
		self.ivalue = 0.0
		self.ioptional = 0

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
		instance.imin = stream.read_float()
		instance.imax = stream.read_float()
		instance.ivalue = stream.read_float()
		instance.ioptional = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.imin)
		stream.write_float(instance.imax)
		stream.write_float(instance.ivalue)
		stream.write_uint(instance.ioptional)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('imin', Float, (0, None))
		yield ('imax', Float, (0, None))
		yield ('ivalue', Float, (0, None))
		yield ('ioptional', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'FloatData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* imin = {fmt_member(self.imin, indent+1)}'
		s += f'\n	* imax = {fmt_member(self.imax, indent+1)}'
		s += f'\n	* ivalue = {fmt_member(self.ivalue, indent+1)}'
		s += f'\n	* ioptional = {fmt_member(self.ioptional, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
