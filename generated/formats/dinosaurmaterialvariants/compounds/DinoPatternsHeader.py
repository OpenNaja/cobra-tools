from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.basic import ZStringObfuscated
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DinoPatternsHeader(MemStruct):

	__name__ = 'DinoPatternsHeader'

	_import_path = 'generated.formats.dinosaurmaterialvariants.compounds.DinoPatternsHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.set_count = 0
		self.pattern_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		self.set_name = Pointer(self.context, 0, ZString)
		self.patterns = Pointer(self.context, self.pattern_count, DinoPatternsHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.PatternArray"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.set_count = 0
		self.pattern_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		self.set_name = Pointer(self.context, 0, ZString)
		self.patterns = Pointer(self.context, self.pattern_count, DinoPatternsHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.PatternArray"])

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fgm_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'set_count', Uint64, (0, None), (False, None)
		yield 'set_name', Pointer, (0, ZString), (False, None)
		yield 'patterns', Pointer, (instance.pattern_count, DinoPatternsHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.PatternArray"]), (False, None)
		yield 'pattern_count', Uint64, (0, None), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'DinoPatternsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
