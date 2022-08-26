from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.dinosaurmaterialvariants.compounds.PatternArray import PatternArray
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
		self.patterns = Pointer(self.context, self.pattern_count, PatternArray)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.set_count = 0
		self.pattern_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		self.set_name = Pointer(self.context, 0, ZString)
		self.patterns = Pointer(self.context, self.pattern_count, PatternArray)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.fgm_name = Pointer.from_stream(stream, instance.context, 0, ZStringObfuscated)
		instance.set_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.set_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.patterns = Pointer.from_stream(stream, instance.context, instance.pattern_count, PatternArray)
		instance.pattern_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zero = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.fgm_name, int):
			instance.fgm_name.arg = 0
		if not isinstance(instance.set_name, int):
			instance.set_name.arg = 0
		if not isinstance(instance.patterns, int):
			instance.patterns.arg = instance.pattern_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.fgm_name)
		Uint64.to_stream(stream, instance.set_count)
		Pointer.to_stream(stream, instance.set_name)
		Pointer.to_stream(stream, instance.patterns)
		Uint64.to_stream(stream, instance.pattern_count)
		Uint64.to_stream(stream, instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'fgm_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'set_count', Uint64, (0, None), (False, None)
		yield 'set_name', Pointer, (0, ZString), (False, None)
		yield 'patterns', Pointer, (instance.pattern_count, PatternArray), (False, None)
		yield 'pattern_count', Uint64, (0, None), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'DinoPatternsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* fgm_name = {self.fmt_member(self.fgm_name, indent+1)}'
		s += f'\n	* set_count = {self.fmt_member(self.set_count, indent+1)}'
		s += f'\n	* set_name = {self.fmt_member(self.set_name, indent+1)}'
		s += f'\n	* patterns = {self.fmt_member(self.patterns, indent+1)}'
		s += f'\n	* pattern_count = {self.fmt_member(self.pattern_count, indent+1)}'
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
