from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.dinosaurmaterialvariants.compound.VariantArray
import generated.formats.ovl_base.basic
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class DinoVariantsHeader(MemStruct):

	"""
	# set_count - seen either 0 or 1, could possibly be more, would need refactor in that case
	# no set_count for rex 93 - has no materialpatterns, so that's probably why it's different
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.has_sets = 0
		self.variant_count = 0
		self.zero = 0
		self.fgm_name = 0
		self.set_name = 0
		self.variants = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.has_sets = 0
		self.variant_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)
		self.set_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.variants = Pointer(self.context, self.variant_count, generated.formats.dinosaurmaterialvariants.compound.VariantArray.VariantArray)

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
		instance.fgm_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)
		instance.has_sets = stream.read_uint64()
		instance.set_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.variants = Pointer.from_stream(stream, instance.context, instance.variant_count, generated.formats.dinosaurmaterialvariants.compound.VariantArray.VariantArray)
		instance.variant_count = stream.read_uint64()
		instance.zero = stream.read_uint64()
		instance.fgm_name.arg = 0
		instance.set_name.arg = 0
		instance.variants.arg = instance.variant_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.fgm_name)
		stream.write_uint64(instance.has_sets)
		Pointer.to_stream(stream, instance.set_name)
		Pointer.to_stream(stream, instance.variants)
		stream.write_uint64(instance.variant_count)
		stream.write_uint64(instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('fgm_name', Pointer, (0, generated.formats.ovl_base.basic.ZStringObfuscated))
		yield ('has_sets', Uint64, (0, None))
		yield ('set_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('variants', Pointer, (instance.variant_count, generated.formats.dinosaurmaterialvariants.compound.VariantArray.VariantArray))
		yield ('variant_count', Uint64, (0, None))
		yield ('zero', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'DinoVariantsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* fgm_name = {fmt_member(self.fgm_name, indent+1)}'
		s += f'\n	* has_sets = {fmt_member(self.has_sets, indent+1)}'
		s += f'\n	* set_name = {fmt_member(self.set_name, indent+1)}'
		s += f'\n	* variants = {fmt_member(self.variants, indent+1)}'
		s += f'\n	* variant_count = {fmt_member(self.variant_count, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
