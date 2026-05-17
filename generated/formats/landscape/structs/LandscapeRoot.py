from generated.array import Array
from generated.formats.landscape.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class LandscapeRoot(MemStruct):

	"""
	232 bytes
	"""

	__name__ = 'LandscapeRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.pointers_1 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.pointers_2 = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.size = name_type_map['Uint'](self.context, 0, None)
		self.a = name_type_map['Ushort'](self.context, 0, None)
		self.b = name_type_map['Ushort'](self.context, 0, None)
		self.rest = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.name_buffer_size = name_type_map['Ushort'](self.context, 0, None)
		self.rest_2 = Array(self.context, 0, None, (0,), name_type_map['Ushort'])
		self.things_count = name_type_map['Ushort'](self.context, 0, None)
		self.rest_3 = Array(self.context, 0, None, (0,), name_type_map['Ushort'])

		# links buffers to ms2 dependencies if they are streamed
		self.buffer_pointers = name_type_map['ArrayPointer'](self.context, 3, name_type_map['BufferPresence'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'pointers_1', Array, (0, None, (13,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'buffer_pointers', name_type_map['ArrayPointer'], (3, name_type_map['BufferPresence']), (False, None), (None, None)
		yield 'pointers_2', Array, (0, None, (9,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'size', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'a', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'rest', Array, (0, None, (6,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'name_buffer_size', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'rest_2', Array, (0, None, (8,), name_type_map['Ushort']), (False, None), (None, None)
		yield 'things_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'rest_3', Array, (0, None, (7,), name_type_map['Ushort']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pointers_1', Array, (0, None, (13,), name_type_map['Uint64']), (False, None)
		yield 'buffer_pointers', name_type_map['ArrayPointer'], (3, name_type_map['BufferPresence']), (False, None)
		yield 'pointers_2', Array, (0, None, (9,), name_type_map['Uint64']), (False, None)
		yield 'size', name_type_map['Uint'], (0, None), (False, None)
		yield 'a', name_type_map['Ushort'], (0, None), (False, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None)
		yield 'rest', Array, (0, None, (6,), name_type_map['Ubyte']), (False, None)
		yield 'name_buffer_size', name_type_map['Ushort'], (0, None), (False, None)
		yield 'rest_2', Array, (0, None, (8,), name_type_map['Ushort']), (False, None)
		yield 'things_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'rest_3', Array, (0, None, (7,), name_type_map['Ushort']), (False, None)
