from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class ZerosPadding(BaseStruct):

	__name__ = 'ZerosPadding'

	_import_path = 'generated.formats.ms2.compounds.ZerosPadding'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hier_2_padding_0 = 0

		# 128 still has 16 bytes
		self.hier_2_padding_1 = 0

		# 129 is the first with 24 bytes
		self.hier_2_padding_2 = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'hier_2_padding_0', Uint64, (0, None), (False, None)
		if 64 < instance.arg:
			yield 'hier_2_padding_1', Uint64, (0, None), (False, None)
		if 128 < instance.arg:
			yield 'hier_2_padding_2', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ZerosPadding [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
