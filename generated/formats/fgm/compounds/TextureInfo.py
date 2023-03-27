from generated.array import Array
from generated.formats.base.basic import Uint
from generated.formats.fgm.compounds.Color import Color
from generated.formats.fgm.compounds.GenericInfo import GenericInfo
from generated.formats.fgm.compounds.TexIndex import TexIndex


class TextureInfo(GenericInfo):

	"""
	part of fgm fragment, per texture involved
	"""

	__name__ = 'TextureInfo'

	_import_key = 'fgm.compounds.TextureInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Stores 2 rgba colors

		# Stores rgba color
		self.value = Array(self.context, 0, None, (0,), Color)
		self.some_index_0 = 0
		self.some_index_1 = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('value', Array, (0, None, (1,), TexIndex), (False, None), True)
		yield ('value', Array, (0, None, (2,), Color), (False, None), True)
		yield ('value', Array, (0, None, (1,), Color), (False, None), True)
		yield ('some_index_0', Uint, (0, None), (True, 0), True)
		yield ('some_index_1', Uint, (0, None), (True, 0), True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.dtype == 8:
			yield 'value', Array, (0, None, (1,), TexIndex), (False, None)
		if instance.context.version >= 18 and instance.dtype == 7:
			yield 'value', Array, (0, None, (2,), Color), (False, None)
		if instance.context.version <= 17 and instance.dtype == 7:
			yield 'value', Array, (0, None, (1,), Color), (False, None)
		if instance.context.version >= 18:
			yield 'some_index_0', Uint, (0, None), (True, 0)
			yield 'some_index_1', Uint, (0, None), (True, 0)


TextureInfo.init_attributes()
