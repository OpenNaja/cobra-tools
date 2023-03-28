from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ParticleAtlasRoot(MemStruct):

	__name__ = 'ParticleAtlasRoot'

	_import_key = 'particleatlas.compounds.ParticleAtlasRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# matches number in tex file name
		self.id = 0
		self.zero = 0
		self.tex_name = Pointer(self.context, 0, ZString)
		self.gfr_name = Pointer(self.context, 0, ZString)

		# tex file used by atlas
		self.dependency_name = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('tex_name', Pointer, (0, ZString), (False, None), None)
		yield ('gfr_name', Pointer, (0, ZString), (False, None), None)
		yield ('id', Uint, (0, None), (False, None), None)
		yield ('zero', Uint, (0, None), (False, None), None)
		yield ('dependency_name', Pointer, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'tex_name', Pointer, (0, ZString), (False, None)
		yield 'gfr_name', Pointer, (0, ZString), (False, None)
		yield 'id', Uint, (0, None), (False, None)
		yield 'zero', Uint, (0, None), (False, None)
		yield 'dependency_name', Pointer, (0, None), (False, None)


ParticleAtlasRoot.init_attributes()
