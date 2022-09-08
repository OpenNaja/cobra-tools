import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint


class TypeOther(BaseStruct):

	"""
	generic
	"""

	__name__ = 'TypeOther'

	_import_path = 'generated.formats.bnk.compounds.TypeOther'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of this section
		self.length = 0

		# id of this Sound SFX object
		self.raw = Array(self.context, 0, None, (0,), Byte)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.length = 0
		self.raw = numpy.zeros((self.length,), dtype=numpy.dtype('int8'))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'length', Uint, (0, None), (False, None)
		yield 'raw', Array, (0, None, (instance.length,), Byte), (False, None)

	def get_info_str(self, indent=0):
		return f'TypeOther [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
