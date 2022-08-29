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

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 'BANI'
		self.magic = Array((0,), Byte, self.context, 0, None)

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
		Array.to_stream(stream, instance.magic, (4,), Byte, instance.context, 0, None)
		ZString.to_stream(stream, instance.banis_name)
		BaniRoot.to_stream(stream, instance.data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'magic', Array, ((4,), Byte, 0, None), (False, None)
		yield 'banis_name', ZString, (0, None), (False, None)
		yield 'data', BaniRoot, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BaniInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* magic = {self.fmt_member(self.magic, indent+1)}'
		s += f'\n	* banis_name = {self.fmt_member(self.banis_name, indent+1)}'
		s += f'\n	* data = {self.fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
