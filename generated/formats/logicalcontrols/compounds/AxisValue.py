from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AxisValue(MemStruct):

	__name__ = 'AxisValue'

	_import_key = 'logicalcontrols.compounds.AxisValue'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.u_1 = 0
		self.u_2 = 0
		self.u_3 = 0
		self.u_4 = 0
		self.axis_name = Pointer(self.context, 0, ZString)
		self.value_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('axis_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('u_0', Uint64, (0, None), (False, None), (None, None))
		yield ('u_1', Uint64, (0, None), (False, None), (None, None))
		yield ('u_2', Uint64, (0, None), (False, None), (None, None))
		yield ('value_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('u_3', Uint64, (0, None), (False, None), (None, None))
		yield ('u_4', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'axis_name', Pointer, (0, ZString), (False, None)
		yield 'u_0', Uint64, (0, None), (False, None)
		yield 'u_1', Uint64, (0, None), (False, None)
		yield 'u_2', Uint64, (0, None), (False, None)
		yield 'value_name', Pointer, (0, ZString), (False, None)
		yield 'u_3', Uint64, (0, None), (False, None)
		yield 'u_4', Uint64, (0, None), (False, None)


AxisValue.init_attributes()
