import generated.formats.base.basic
import generated.formats.dinosaurmaterialvariants.compound.VariantArray
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class DinoVariantsHeader(MemStruct):

	"""
	# set_count - seen either 0 or 1, could possibly be more, would need refactor in that case
	# no set_count for rex 93 - has no materialpatterns, so that's probably why it's different
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.has_sets = 0
		self.variant_count = 0
		self.zero = 0
		self.name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.set_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.variants = Pointer(self.context, self.variant_count, generated.formats.dinosaurmaterialvariants.compound.VariantArray.VariantArray)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.has_sets = 0
		self.variant_count = 0
		self.zero = 0
		self.name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
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
		instance.name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.has_sets = stream.read_uint64()
		instance.set_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.variants = Pointer.from_stream(stream, instance.context, instance.variant_count, generated.formats.dinosaurmaterialvariants.compound.VariantArray.VariantArray)
		instance.variant_count = stream.read_uint64()
		instance.zero = stream.read_uint64()
		instance.name.arg = 0
		instance.set_name.arg = 0
		instance.variants.arg = instance.variant_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.name)
		stream.write_uint64(instance.has_sets)
		Pointer.to_stream(stream, instance.set_name)
		Pointer.to_stream(stream, instance.variants)
		stream.write_uint64(instance.variant_count)
		stream.write_uint64(instance.zero)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self):
		return f'DinoVariantsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* name = {self.name.__repr__()}'
		s += f'\n	* has_sets = {self.has_sets.__repr__()}'
		s += f'\n	* set_name = {self.set_name.__repr__()}'
		s += f'\n	* variants = {self.variants.__repr__()}'
		s += f'\n	* variant_count = {self.variant_count.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
