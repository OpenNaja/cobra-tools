from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class IslandRoot(MemStruct):

	"""
	JWE2: 32 bytes
	"""

	__name__ = 'IslandRoot'

	_import_path = 'generated.formats.island.compounds.IslandRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = 0.0
		self.b = 0.0
		self.count = 0
		self.zero = 0
		self.path_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'path_name', Pointer, (0, ZString), (False, None)
		yield 'a', Float, (0, None), (False, None)
		yield 'b', Float, (0, None), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'IslandRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
