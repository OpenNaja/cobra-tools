from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CrossFadeData(MemStruct):

	__name__ = 'CrossFadeData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.blend_time = name_type_map['Float'](self.context, 0, None)
		self.flags = name_type_map['Uint'](self.context, 0, None)
		self.curve = name_type_map['Pointer'](self.context, 0, name_type_map['CurveData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'blend_time', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'curve', name_type_map['Pointer'], (0, name_type_map['CurveData']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'blend_time', name_type_map['Float'], (0, None), (False, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None)
		yield 'curve', name_type_map['Pointer'], (0, name_type_map['CurveData']), (False, None)
