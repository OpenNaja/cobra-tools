import logging
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.motiongraph.imports import name_type_map

from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Activity(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'Activity'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_2 = name_type_map['Uint64'].from_value(0)
		self.count_3 = name_type_map['Uint64'].from_value(0)
		self.index_a = name_type_map['Int'].from_value(-1)
		self.index_b = name_type_map['Int'].from_value(-1)
		self.data_type = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])

		# template has to be defined according to data type ie 'AnimationActivity' + 'Data'
		self.data = name_type_map['Pointer'](self.context, 0, None)
		self.name_b = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'data_type', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'data', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'count_2', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'count_3', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'index_a', name_type_map['Int'], (0, None), (True, -1), (None, None)
		yield 'index_b', name_type_map['Int'], (0, None), (True, -1), (None, None)
		yield 'name_b', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data_type', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'data', name_type_map['Pointer'], (0, None), (False, None)
		yield 'count_2', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'count_3', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'index_a', name_type_map['Int'], (0, None), (True, -1)
		yield 'index_b', name_type_map['Int'], (0, None), (True, -1)
		yield 'name_b', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		if prop == "data":
			activity = self.data_type.data
			key = f"{activity}Data"
			try:
				return name_type_map[key]
			except KeyError:
				logging.debug(f"Motiongraph.{activity} is not supported")

