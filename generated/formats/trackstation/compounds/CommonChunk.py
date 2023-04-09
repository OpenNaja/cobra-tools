import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CommonChunk(MemStruct):

	__name__ = 'CommonChunk'

	_import_key = 'trackstation.compounds.CommonChunk'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float_1 = 0.0
		self.float_2 = 0.0
		self.unk_flags_0 = Array(self.context, 0, None, (0,), Ubyte)
		self.unk_flags_1 = Array(self.context, 0, None, (0,), Ubyte)
		self.zero = 0
		self.piece_name_0 = Pointer(self.context, 0, ZString)
		self.piece_name_1 = Pointer(self.context, 0, ZString)
		self.piece_name_2 = Pointer(self.context, 0, ZString)
		self.piece_name_3 = Pointer(self.context, 0, ZString)
		self.piece_name_4 = Pointer(self.context, 0, ZString)
		self.piece_name_5 = Pointer(self.context, 0, ZString)
		self.piece_name_6 = Pointer(self.context, 0, ZString)
		self.piece_name_7 = Pointer(self.context, 0, ZString)
		self.piece_name_8 = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('float_1', Float, (0, None), (False, None), (None, None))
		yield ('float_2', Float, (0, None), (False, None), (None, None))
		yield ('piece_name_0', Pointer, (0, ZString), (False, None), (None, None))
		yield ('piece_name_1', Pointer, (0, ZString), (False, None), (None, None))
		yield ('piece_name_2', Pointer, (0, ZString), (False, None), (None, None))
		yield ('unk_flags_0', Array, (0, None, (8,), Ubyte), (False, None), (None, None))
		yield ('piece_name_3', Pointer, (0, ZString), (False, None), (None, None))
		yield ('piece_name_4', Pointer, (0, ZString), (False, None), (None, None))
		yield ('piece_name_5', Pointer, (0, ZString), (False, None), (None, None))
		yield ('unk_flags_1', Array, (0, None, (8,), Ubyte), (False, None), (None, None))
		yield ('piece_name_6', Pointer, (0, ZString), (False, None), (None, None))
		yield ('piece_name_7', Pointer, (0, ZString), (False, None), (None, None))
		yield ('piece_name_8', Pointer, (0, ZString), (False, None), (None, None))
		yield ('zero', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'float_1', Float, (0, None), (False, None)
		yield 'float_2', Float, (0, None), (False, None)
		yield 'piece_name_0', Pointer, (0, ZString), (False, None)
		yield 'piece_name_1', Pointer, (0, ZString), (False, None)
		yield 'piece_name_2', Pointer, (0, ZString), (False, None)
		yield 'unk_flags_0', Array, (0, None, (8,), Ubyte), (False, None)
		yield 'piece_name_3', Pointer, (0, ZString), (False, None)
		yield 'piece_name_4', Pointer, (0, ZString), (False, None)
		yield 'piece_name_5', Pointer, (0, ZString), (False, None)
		yield 'unk_flags_1', Array, (0, None, (8,), Ubyte), (False, None)
		yield 'piece_name_6', Pointer, (0, ZString), (False, None)
		yield 'piece_name_7', Pointer, (0, ZString), (False, None)
		yield 'piece_name_8', Pointer, (0, ZString), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)
