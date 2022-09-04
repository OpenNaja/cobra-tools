from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class EventEntry(MemStruct):

	"""
	PC: 56 bytes
	JWE2: 40 bytes
	# todo - improve versioning
	"""

	__name__ = 'EventEntry'

	_import_path = 'generated.formats.wmeta.compounds.EventEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hash = 0
		self.zero = 0
		self.zero_2 = 0
		self.size = 0
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.zero_3 = 0
		self.flag_3 = 0
		self.hash_b = 0
		self.hash_c = 0
		self.zero_4 = 0
		self.u_2 = 0
		self.u_1 = 0
		self.block_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.hash = 0
		self.zero = 0
		if self.context.version <= 18:
			self.zero_2 = 0
			self.size = 0
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		if self.context.version <= 18:
			self.zero_3 = 0
			self.flag_3 = 0
		self.hash_b = 0
		self.hash_c = 0
		self.zero_4 = 0
		if self.context.version >= 19:
			self.u_2 = 0
			self.u_1 = 0
		if self.context.version <= 18:
			self.block_name = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.hash = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 18:
			instance.block_name = Pointer.from_stream(stream, instance.context, 0, ZString)
			instance.zero_2 = Ushort.from_stream(stream, instance.context, 0, None)
			instance.size = Ushort.from_stream(stream, instance.context, 0, None)
		instance.flag_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.flag_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.flag_2 = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 18:
			instance.zero_3 = Uint64.from_stream(stream, instance.context, 0, None)
			instance.flag_3 = Uint.from_stream(stream, instance.context, 0, None)
		instance.hash_b = Uint.from_stream(stream, instance.context, 0, None)
		instance.hash_c = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero_4 = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 19:
			instance.u_2 = Uint.from_stream(stream, instance.context, 0, None)
			instance.u_1 = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.block_name, int):
			instance.block_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.hash)
		Uint.to_stream(stream, instance.zero)
		if instance.context.version <= 18:
			Pointer.to_stream(stream, instance.block_name)
			Ushort.to_stream(stream, instance.zero_2)
			Ushort.to_stream(stream, instance.size)
		Uint.to_stream(stream, instance.flag_0)
		Uint.to_stream(stream, instance.flag_1)
		Uint.to_stream(stream, instance.flag_2)
		if instance.context.version <= 18:
			Uint64.to_stream(stream, instance.zero_3)
			Uint.to_stream(stream, instance.flag_3)
		Uint.to_stream(stream, instance.hash_b)
		Uint.to_stream(stream, instance.hash_c)
		Uint.to_stream(stream, instance.zero_4)
		if instance.context.version >= 19:
			Uint.to_stream(stream, instance.u_2)
			Uint.to_stream(stream, instance.u_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'hash', Uint, (0, None), (False, None)
		yield 'zero', Uint, (0, None), (False, None)
		if instance.context.version <= 18:
			yield 'block_name', Pointer, (0, ZString), (False, None)
			yield 'zero_2', Ushort, (0, None), (False, None)
			yield 'size', Ushort, (0, None), (False, None)
		yield 'flag_0', Uint, (0, None), (False, None)
		yield 'flag_1', Uint, (0, None), (False, None)
		yield 'flag_2', Uint, (0, None), (False, None)
		if instance.context.version <= 18:
			yield 'zero_3', Uint64, (0, None), (False, None)
			yield 'flag_3', Uint, (0, None), (False, None)
		yield 'hash_b', Uint, (0, None), (False, None)
		yield 'hash_c', Uint, (0, None), (False, None)
		yield 'zero_4', Uint, (0, None), (False, None)
		if instance.context.version >= 19:
			yield 'u_2', Uint, (0, None), (False, None)
			yield 'u_1', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'EventEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
