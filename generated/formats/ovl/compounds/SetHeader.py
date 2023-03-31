from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ovl.compounds.AssetEntry import AssetEntry
from generated.formats.ovl.compounds.SetEntry import SetEntry


class SetHeader(BaseStruct):

	"""
	defines amount of sets and assets
	"""

	__name__ = 'SetHeader'

	_import_key = 'ovl.compounds.SetHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.set_count = 0
		self.asset_count = 0

		# must be 1065336831
		self.sig_a = 1065336831

		# must be 16909320
		self.sig_b = 16909320
		self.sets = Array(self.context, 0, None, (0,), SetEntry)
		self.assets = Array(self.context, 0, None, (0,), AssetEntry)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('set_count', Uint, (0, None), (False, None), (None, None))
		yield ('asset_count', Uint, (0, None), (False, None), (None, None))
		yield ('sig_a', Uint, (0, None), (False, 1065336831), (None, None))
		yield ('sig_b', Uint, (0, None), (False, 16909320), (None, None))
		yield ('sets', Array, (0, None, (None,), SetEntry), (False, None), (None, None))
		yield ('assets', Array, (0, None, (None,), AssetEntry), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'set_count', Uint, (0, None), (False, None)
		yield 'asset_count', Uint, (0, None), (False, None)
		yield 'sig_a', Uint, (0, None), (False, 1065336831)
		yield 'sig_b', Uint, (0, None), (False, 16909320)
		yield 'sets', Array, (0, None, (instance.set_count,), SetEntry), (False, None)
		yield 'assets', Array, (0, None, (instance.asset_count,), AssetEntry), (False, None)


SetHeader.init_attributes()
