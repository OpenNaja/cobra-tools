from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class ArchiveMeta(BaseStruct):

	"""
	Apparently sizes or offsets for each archive
	"""

	__name__ = 'ArchiveMeta'

	_import_key = 'ovl.compounds.ArchiveMeta'
	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# seemingly unused in JWE
		self.unk_0 = 0

		# seemingly unused in JWE, subtracting this from ovs uncompressed_size to get length of the uncompressed ovs header
		self.unk_1 = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('unk_0', Uint, (0, None), (False, None), (None, None))
		yield ('unk_1', Uint, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_0', Uint, (0, None), (False, None)
		yield 'unk_1', Uint, (0, None), (False, None)
