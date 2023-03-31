from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TexturestreamHeader(MemStruct):

	"""
	JWE1, PZ, PC: 8 bytes
	JWE2: 16 bytes
	"""

	__name__ = 'TexturestreamHeader'

	_import_key = 'tex.compounds.TexturestreamHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero = 0
		self.lod_index = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('zero', Uint64, (0, None), (True, 0), None)
		yield ('lod_index', Uint64, (0, None), (False, None), True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zero', Uint64, (0, None), (True, 0)
		if instance.context.user_version.use_djb and (instance.context.version == 20):
			yield 'lod_index', Uint64, (0, None), (False, None)


TexturestreamHeader.init_attributes()
