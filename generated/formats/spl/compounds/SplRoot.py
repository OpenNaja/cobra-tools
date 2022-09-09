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
