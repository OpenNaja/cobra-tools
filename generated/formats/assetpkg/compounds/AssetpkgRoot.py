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

	def set_defaults(self):
		super().set_defaults()
		self._zero = 0
		self.asset_path = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.asset_path = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance._zero = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.asset_path, int):
			instance.asset_path.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.asset_path)
		Uint64.to_stream(stream, instance._zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'asset_path', Pointer, (0, ZString), (False, None)
		yield '_zero', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'AssetpkgRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
