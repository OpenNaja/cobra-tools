from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BufferPresence(MemStruct):

	__name__ = 'BufferPresence'

	_import_key = 'ms2.compounds.BufferPresence'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# in DLA and JWE2, this can be a dependency to a model2stream
		self.dependency_name = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('dependency_name', Pointer, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'dependency_name', Pointer, (0, None), (False, None)


BufferPresence.init_attributes()
