
import logging

from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry
from generated.struct import StructBase

from generated.struct import StructBase


class StreamDebugger(StructBase):

	"""
	logs stream address to debug log
	"""

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		pass

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		pass

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)

	def get_info_str(self, indent=0):
		return f'StreamDebugger [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

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
		self.io_start = stream.tell()
		logging.debug(f"Debugger at {stream.tell()}")
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()

		self.io_size = stream.tell() - self.io_start


