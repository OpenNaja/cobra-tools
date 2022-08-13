import generated.formats.motiongraph.compounds.CurveDataPoints
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CurveData(MemStruct):

	"""
	16 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.points = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.points = Pointer(self.context, self.count, generated.formats.motiongraph.compounds.CurveDataPoints.CurveDataPoints)

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
		instance.count = stream.read_uint64()
		instance.points = Pointer.from_stream(stream, instance.context, instance.count, generated.formats.motiongraph.compounds.CurveDataPoints.CurveDataPoints)
		instance.points.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.count)
		Pointer.to_stream(stream, instance.points)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('count', Uint64, (0, None))
		yield ('points', Pointer, (instance.count, generated.formats.motiongraph.compounds.CurveDataPoints.CurveDataPoints))

	def get_info_str(self, indent=0):
		return f'CurveData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* points = {self.fmt_member(self.points, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
