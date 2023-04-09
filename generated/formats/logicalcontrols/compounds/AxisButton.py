from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AxisButton(MemStruct):

	"""
	24 bytes, can be padded to 32
	"""

	__name__ = 'AxisButton'

	_import_key = 'logicalcontrols.compounds.AxisButton'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.button_name = Pointer(self.context, 0, ZString)
		self.axis_name_x = Pointer(self.context, 0, ZString)
		self.axis_name_y = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('button_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('axis_name_x', Pointer, (0, ZString), (False, None), (None, None))
		yield ('axis_name_y', Pointer, (0, ZString), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'button_name', Pointer, (0, ZString), (False, None)
		yield 'axis_name_x', Pointer, (0, ZString), (False, None)
		yield 'axis_name_y', Pointer, (0, ZString), (False, None)
