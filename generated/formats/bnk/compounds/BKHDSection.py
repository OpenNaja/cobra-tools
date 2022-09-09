import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint


class BKHDSection(BaseStruct):

	"""
	First Section of a soundbank aux
	"""

	__name__ = 'BKHDSection'

	_import_path = 'generated.formats.bnk.compounds.BKHDSection'

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'length', Uint, (0, None), (False, None)
		yield 'version', Uint, (0, None), (False, None)
		yield 'id_a', Uint, (0, None), (False, None)
		yield 'id_b', Uint, (0, None), (False, None)
		yield 'constant_a', Uint, (0, None), (False, None)
		yield 'constant_b', Uint, (0, None), (False, None)
		yield 'unk', Uint, (0, None), (False, None)
		yield 'zeroes', Array, (0, None, (instance.length - 24,), Ubyte), (False, None)

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0
		self.unk = 0

		# sometimes present
		# self.zeroes = numpy.zeros((self.length - 24,), dtype=numpy.dtype('uint8'))


