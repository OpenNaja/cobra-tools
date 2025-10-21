from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackedridecar.imports import name_type_map


class TrackedRideCarRoot(MemStruct):

	__name__ = 'TrackedRideCarRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Numer of seats rows
		self.seat_rows_count = name_type_map['Uint'](self.context, 0, None)

		# Total number of seats in this car
		self.total_seats_count = name_type_map['Uint'](self.context, 0, None)

		# Size of different fence elements
		self.sizes = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.zero_0 = name_type_map['Uint'].from_value(0)
		self.zero_2 = name_type_map['Uint64'].from_value(0)
		self.seat_rows = name_type_map['ArrayPointer'](self.context, self.seat_rows_count, name_type_map['Row'])
		self.hitcheck_model_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.cabin_geometry_attach = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.cabin_geometry = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'seat_rows', name_type_map['ArrayPointer'], (None, name_type_map['Row']), (False, None), (None, None)
		yield 'seat_rows_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'total_seats_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'sizes', Array, (0, None, (3,), name_type_map['Float']), (False, None), (None, None)
		yield 'zero_0', name_type_map['Uint'], (0, None), (True, 0), (None, None)
		yield 'hitcheck_model_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'cabin_geometry_attach', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: context.version >= 7, None)
		yield 'cabin_geometry', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (lambda context: context.version >= 7, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (True, 0), (lambda context: context.version >= 7, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'seat_rows', name_type_map['ArrayPointer'], (instance.seat_rows_count, name_type_map['Row']), (False, None)
		yield 'seat_rows_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'total_seats_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'sizes', Array, (0, None, (3,), name_type_map['Float']), (False, None)
		yield 'zero_0', name_type_map['Uint'], (0, None), (True, 0)
		yield 'hitcheck_model_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if instance.context.version >= 7:
			yield 'cabin_geometry_attach', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
			yield 'cabin_geometry', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
			yield 'zero_2', name_type_map['Uint64'], (0, None), (True, 0)
