# START_GLOBALS
import logging

from generated.formats.ms2.compounds.HitCheckEntry import HitCheckEntry
from generated.base_struct import BaseStruct

# END_GLOBALS

class StreamDebugger(BaseStruct):

	# START_CLASS

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		pass

	def read(self, stream):
		logging.warning(f"StreamDebugger.read is deprecated")
		self.io_start = stream.tell()
		logging.debug(f"Debugger at {stream.tell()}")
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		logging.warning(f"StreamDebugger.write is deprecated")
		self.io_start = stream.tell()

		self.io_size = stream.tell() - self.io_start

