from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class STIDRef(BaseStruct):

	__name__ = 'STIDRef'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# fnv1
		self.bank_i_d = name_type_map['Uint'](self.context, 0, None)
		self.stringsize = name_type_map['Ubyte'](self.context, 0, None)
		self.name = Array(self.context, 0, None, (0,), name_type_map['Char'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'bank_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'stringsize', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'name', Array, (0, None, (None,), name_type_map['Char']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'bank_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'stringsize', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'name', Array, (0, None, (instance.stringsize,), name_type_map['Char']), (False, None)
