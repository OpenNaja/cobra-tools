from generated.formats.base.basic import Uint
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class GenericInfo(MemStruct):

	__name__ = 'GenericInfo'

	_import_path = 'generated.formats.fgm.compounds.GenericInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# byte offset to name in fgm buffer
		self._name_offset = 0
		self.dtype = FgmDtype(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield '_name_offset', Uint, (0, None), (False, None)
		yield 'dtype', FgmDtype, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'GenericInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
