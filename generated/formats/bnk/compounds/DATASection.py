import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint


class DATASection(BaseStruct):

	"""
	second Section of a soundback aux
	"""

	__name__ = 'DATASection'

	_import_path = 'generated.formats.bnk.compounds.DATASection'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of following data
		self.length = 0
		self.wem_datas = Array(self.context, 0, None, (0,), Byte)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.length = 0
		self.wem_datas = numpy.zeros((self.length,), dtype=numpy.dtype('int8'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.length = Uint.from_stream(stream, instance.context, 0, None)
		instance.wem_datas = Array.from_stream(stream, instance.context, 0, None, (instance.length,), Byte)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.length)
		Array.to_stream(stream, instance.wem_datas, Byte)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'length', Uint, (0, None), (False, None)
		yield 'wem_datas', Array, (0, None, (instance.length,), Byte), (False, None)

	def get_info_str(self, indent=0):
		return f'DATASection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
