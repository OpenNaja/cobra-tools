import generated.formats.spl.compounds.SplData
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SplRoot(MemStruct):

	"""
	JWE2: 16 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.sixteen = 0
		self.one = 0

		# total length of the interpolated curve, cf blender curvetools.CurveLength
		self.length = 0.0
		self.spline_data = Pointer(self.context, self.count, generated.formats.spl.compounds.SplData.SplData)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.sixteen = 0
		self.one = 0
		self.length = 0.0
		self.spline_data = Pointer(self.context, self.count, generated.formats.spl.compounds.SplData.SplData)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.spline_data = Pointer.from_stream(stream, instance.context, instance.count, generated.formats.spl.compounds.SplData.SplData)
		instance.count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.sixteen = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.one = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.length = Float.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.spline_data, int):
			instance.spline_data.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.spline_data)
		stream.write_ushort(instance.count)
		stream.write_ubyte(instance.sixteen)
		stream.write_ubyte(instance.one)
		stream.write_float(instance.length)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'spline_data', Pointer, (instance.count, generated.formats.spl.compounds.SplData.SplData)
		yield 'count', Ushort, (0, None)
		yield 'sixteen', Ubyte, (0, None)
		yield 'one', Ubyte, (0, None)
		yield 'length', Float, (0, None)

	def get_info_str(self, indent=0):
		return f'SplRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* spline_data = {self.fmt_member(self.spline_data, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* sixteen = {self.fmt_member(self.sixteen, indent+1)}'
		s += f'\n	* one = {self.fmt_member(self.one, indent+1)}'
		s += f'\n	* length = {self.fmt_member(self.length, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
