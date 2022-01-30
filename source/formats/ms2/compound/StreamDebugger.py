# START_GLOBALS
import logging

from generated.context import ContextReference
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry

# END_GLOBALS

class StreamDebugger:

	context = ContextReference()

	# START_CLASS

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
		logging.debug(f"Debugger at {stream.tell()}")
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()

		self.io_size = stream.tell() - self.io_start

