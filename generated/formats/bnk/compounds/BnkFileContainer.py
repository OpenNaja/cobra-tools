from generated.formats.bnk.compounds.BnkBufferData import BnkBufferData
from generated.formats.ovl_base.compounds.GenericHeader import GenericHeader


class BnkFileContainer(GenericHeader):

	"""
	custom struct
	"""

	__name__ = 'BnkFileContainer'

	_import_path = 'generated.formats.bnk.compounds.BnkFileContainer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.bnk_header = BnkBufferData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.bnk_header = BnkBufferData(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.bnk_header = BnkBufferData.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		BnkBufferData.to_stream(stream, instance.bnk_header)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'bnk_header', BnkBufferData, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BnkFileContainer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
