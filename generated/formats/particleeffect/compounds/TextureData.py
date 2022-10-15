from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TextureData(MemStruct):

	__name__ = 'TextureData'

	_import_key = 'particleeffect.compounds.TextureData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# only present if textured
		self.dependency_name = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('dependency_name', Pointer, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'dependency_name', Pointer, (0, None), (False, None)
