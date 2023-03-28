from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class StringData(MemStruct):

	"""
	16 bytes in log
	"""

	__name__ = 'StringData'

	_import_key = 'specdef.compounds.StringData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ioptional = 0
		self.str_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('str_name', Pointer, (0, ZString), (False, None), None)
		yield ('ioptional', Uint, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'str_name', Pointer, (0, ZString), (False, None)
		yield 'ioptional', Uint, (0, None), (False, None)


StringData.init_attributes()
