from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackedridecar.imports import name_type_map


class Row(MemStruct):

	__name__ = 'Row'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Offset of the row to create station gates
		self.offset = name_type_map['Float'](self.context, 0, None)
		self.u_0 = name_type_map['Uint'].from_value(0)
		self.seats_count = name_type_map['Uint64'](self.context, 0, None)
		self.seats = name_type_map['ArrayPointer'](self.context, self.seats_count, name_type_map['Seat'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'offset', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'u_0', name_type_map['Uint'], (0, None), (True, 0), (None, None)
		yield 'seats', name_type_map['ArrayPointer'], (None, name_type_map['Seat']), (False, None), (None, None)
		yield 'seats_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', name_type_map['Float'], (0, None), (False, None)
		yield 'u_0', name_type_map['Uint'], (0, None), (True, 0)
		yield 'seats', name_type_map['ArrayPointer'], (instance.seats_count, name_type_map['Seat']), (False, None)
		yield 'seats_count', name_type_map['Uint64'], (0, None), (False, None)
