from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FloatData(MemStruct):

	"""
	16 bytes in log
	"""

	__name__ = 'FloatData'

	_import_key = 'specdef.compounds.FloatData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.imin = 0.0
		self.imax = 0.0
		self.ivalue = 0.0
		self.ioptional = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('imin', Float, (0, None), (False, None), (None, None))
		yield ('imax', Float, (0, None), (False, None), (None, None))
		yield ('ivalue', Float, (0, None), (False, None), (None, None))
		yield ('ioptional', Uint, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'imin', Float, (0, None), (False, None)
		yield 'imax', Float, (0, None), (False, None)
		yield 'ivalue', Float, (0, None), (False, None)
		yield 'ioptional', Uint, (0, None), (False, None)


FloatData.init_attributes()
