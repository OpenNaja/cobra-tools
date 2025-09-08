from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class DataStreamResourceData(MemStruct):

	"""
	56 bytes
	"""

	__name__ = 'DataStreamResourceData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.curve_type = name_type_map['Uint64'](self.context, 0, None)
		self.curve = name_type_map['CurveData'](self.context, 0, None)
		self.ds_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.type = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.bone_i_d = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.location = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'curve_type', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'ds_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'type', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'bone_i_d', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'location', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'curve', name_type_map['CurveData'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'curve_type', name_type_map['Uint64'], (0, None), (False, None)
		yield 'ds_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'type', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'bone_i_d', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'location', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'curve', name_type_map['CurveData'], (0, None), (False, None)
