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

	_import_key = 'wmeta.compounds.EventEntry'

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

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('hash', Uint, (0, None), (False, None), (None, None))
		yield ('zero', Uint, (0, None), (False, None), (None, None))
		yield ('block_name', Pointer, (0, ZString), (False, None), (lambda context: context.version <= 18, None))
		yield ('zero_2', Ushort, (0, None), (False, None), (lambda context: context.version <= 18, None))
		yield ('size', Ushort, (0, None), (False, None), (lambda context: context.version <= 18, None))
		yield ('flag_0', Uint, (0, None), (False, None), (None, None))
		yield ('flag_1', Uint, (0, None), (False, None), (None, None))
		yield ('flag_2', Uint, (0, None), (False, None), (None, None))
		yield ('zero_3', Uint64, (0, None), (False, None), (lambda context: context.version <= 18, None))
		yield ('flag_3', Uint, (0, None), (False, None), (lambda context: context.version <= 18, None))
		yield ('hash_b', Uint, (0, None), (False, None), (None, None))
		yield ('hash_c', Uint, (0, None), (False, None), (None, None))
		yield ('zero_4', Uint, (0, None), (False, None), (None, None))
		yield ('u_2', Uint, (0, None), (False, None), (lambda context: context.version >= 19, None))
		yield ('u_1', Uint, (0, None), (False, None), (lambda context: context.version >= 19, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
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
