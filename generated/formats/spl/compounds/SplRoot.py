from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SplRoot(MemStruct):

	"""
	JWE2: 16 bytes
	"""

	__name__ = 'SplRoot'

	_import_path = 'generated.formats.spl.compounds.SplRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.sixteen = 16
		self.one = 1

		# total length of the interpolated curve, cf blender Spline.calc_length()
		self.length = 0.0
		self.spline_data = Pointer(self.context, self.count, SplRoot._import_path_map["generated.formats.spl.compounds.SplData"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.sixteen = 16
		self.one = 1
		self.length = 0.0
		self.spline_data = Pointer(self.context, self.count, SplRoot._import_path_map["generated.formats.spl.compounds.SplData"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.spline_data = Pointer.from_stream(stream, instance.context, instance.count, SplRoot._import_path_map["generated.formats.spl.compounds.SplData"])
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
		Ushort.to_stream(stream, instance.count)
		Ubyte.to_stream(stream, instance.sixteen)
		Ubyte.to_stream(stream, instance.one)
		Float.to_stream(stream, instance.length)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'spline_data', Pointer, (instance.count, SplRoot._import_path_map["generated.formats.spl.compounds.SplData"]), (False, None)
		yield 'count', Ushort, (0, None), (False, None)
		yield 'sixteen', Ubyte, (0, None), (False, 16)
		yield 'one', Ubyte, (0, None), (False, 1)
		yield 'length', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'SplRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
