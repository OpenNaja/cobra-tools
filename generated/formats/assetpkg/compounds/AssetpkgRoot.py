from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AssetpkgRoot(MemStruct):

	__name__ = 'AssetpkgRoot'

	_import_path = 'generated.formats.assetpkg.compounds.AssetpkgRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self._zero = 0
		self.asset_path = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'asset_path', Pointer, (0, ZString), (False, None)
		yield '_zero', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'AssetpkgRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
