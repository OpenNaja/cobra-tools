import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bani.compounds.BaniRoot import BaniRoot
from generated.formats.base.basic import Byte
from generated.formats.base.basic import ZString


class BaniInfoHeader(BaseStruct):

	"""
	Custom header struct
	includes fragments but none of the 3 data buffers
	"""

	__name__ = 'BaniInfoHeader'

	_import_path = 'generated.formats.bani.compounds.BaniInfoHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 'BANI'
		self.magic = Array(self.context, 0, None, (0,), Byte)

		# name of the banis file buffer
		self.banis_name = ''
		self.data = BaniRoot(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.magic = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.banis_name = ''
		self.data = BaniRoot(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.magic = Array.from_stream(stream, instance.context, 0, None, (4,), Byte)
		instance.banis_name = ZString.from_stream(stream, instance.context, 0, None)
		instance.data = BaniRoot.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.magic, Byte)
		ZString.to_stream(stream, instance.banis_name)
		BaniRoot.to_stream(stream, instance.data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'magic', Array, (0, None, (4,), Byte), (False, None)
		yield 'banis_name', ZString, (0, None), (False, None)
		yield 'data', BaniRoot, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BaniInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
