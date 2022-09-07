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

	_import_path = 'generated.formats.ovl.compounds.SetHeader'

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

	def set_defaults(self):
		super().set_defaults()
		self.set_count = 0
		self.asset_count = 0
		self.sig_a = 1065336831
		self.sig_b = 16909320
		self.sets = Array(self.context, 0, None, (self.set_count,), SetEntry)
		self.assets = Array(self.context, 0, None, (self.asset_count,), AssetEntry)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.set_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.asset_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.sig_a = Uint.from_stream(stream, instance.context, 0, None)
		instance.sig_b = Uint.from_stream(stream, instance.context, 0, None)
		instance.sets = Array.from_stream(stream, instance.context, 0, None, (instance.set_count,), SetEntry)
		instance.assets = Array.from_stream(stream, instance.context, 0, None, (instance.asset_count,), AssetEntry)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.set_count)
		Uint.to_stream(stream, instance.asset_count)
		Uint.to_stream(stream, instance.sig_a)
		Uint.to_stream(stream, instance.sig_b)
		Array.to_stream(stream, instance.sets, SetEntry)
		Array.to_stream(stream, instance.assets, AssetEntry)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'set_count', Uint, (0, None), (False, None)
		yield 'asset_count', Uint, (0, None), (False, None)
		yield 'sig_a', Uint, (0, None), (False, 1065336831)
		yield 'sig_b', Uint, (0, None), (False, 16909320)
		yield 'sets', Array, (0, None, (instance.set_count,), SetEntry), (False, None)
		yield 'assets', Array, (0, None, (instance.asset_count,), AssetEntry), (False, None)

	def get_info_str(self, indent=0):
		return f'SetHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
