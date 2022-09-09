from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Texture(MemStruct):

	__name__ = 'Texture'

	_import_path = 'generated.formats.matcol.compounds.Texture'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# first fgm slot
		self.fgm_name = Pointer(self.context, 0, ZString)
		self.texture_suffix = Pointer(self.context, 0, ZString)
		self.texture_type = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fgm_name', Pointer, (0, ZString), (False, None)
		yield 'texture_suffix', Pointer, (0, ZString), (False, None)
		yield 'texture_type', Pointer, (0, ZString), (False, None)
