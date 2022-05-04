from source.formats.base.basic import fmt_member
import numpy
from generated.context import ContextReference


class BKHDSection:

	# START_CLASS

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

