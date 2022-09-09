from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class ZlibInfo(BaseStruct):

	"""
	Description of one zlib archive
	"""

	__name__ = 'ZlibInfo'

	_import_path = 'generated.formats.ovl.compounds.ZlibInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# seemingly unused in JWE
		self.zlib_thing_1 = 0

		# seemingly unused in JWE, subtracting this from ovs uncompressed_size to get length of the uncompressed ovs header
		self.zlib_thing_2 = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zlib_thing_1', Uint, (0, None), (False, None)
		yield 'zlib_thing_2', Uint, (0, None), (False, None)
