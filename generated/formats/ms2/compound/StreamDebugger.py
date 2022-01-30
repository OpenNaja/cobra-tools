
import logging

from generated.context import ContextReference
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry

from generated.context import ContextReference


class StreamDebugger:

	"""
	logs stream address to debug log
	"""

	context = ContextReference()

	def get_info_str(self):
		return f'StreamDebugger [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.set_defaults()

	def set_defaults(self):
		pass

	def read(self, stream):
		self.io_start = stream.tell()
		logging.debug(f"{self.name} at {stream.tell()}")
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()

		self.io_size = stream.tell() - self.io_start


