from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ButtonData(MemStruct):

	"""
	# Apparently the binding value is from a = 1..
	# HUD_MapMode:          13  209     m and M
	# HUD_Notifications:    14  210     n and N
	"""

	__name__ = 'ButtonData'

	_import_key = 'logicalcontrols.compounds.ButtonData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.k_1_a = 0
		self.k_1_b = 0
		self.k_2 = 0
		self.k_3 = 0
		self.k_4 = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('k_1_a', Ushort, (0, None), (False, None), None)
		yield ('k_1_b', Ushort, (0, None), (False, None), None)
		yield ('k_2', Uint, (0, None), (False, None), None)
		yield ('k_3', Uint, (0, None), (False, None), None)
		yield ('k_4', Uint, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'k_1_a', Ushort, (0, None), (False, None)
		yield 'k_1_b', Ushort, (0, None), (False, None)
		yield 'k_2', Uint, (0, None), (False, None)
		yield 'k_3', Uint, (0, None), (False, None)
		yield 'k_4', Uint, (0, None), (False, None)


ButtonData.init_attributes()
