from generated.array import Array
from generated.formats.motiongraph.compounds.CurveDataPoint import CurveDataPoint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class CurveDataPoints(MemStruct):

	"""
	array
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = Array((self.arg,), CurveDataPoint, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.data = Array((self.arg,), CurveDataPoint, self.context, 0, None)

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
		instance.data = Array.from_stream(stream, (instance.arg,), CurveDataPoint, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.data, (instance.arg,), CurveDataPoint, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield 'data', Array, ((instance.arg,), CurveDataPoint, 0, None)

	def get_info_str(self, indent=0):
		return f'CurveDataPoints [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* data = {self.fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
