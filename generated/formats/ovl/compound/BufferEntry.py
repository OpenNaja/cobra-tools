

import logging

from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class BufferEntry:

	"""
	8 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index of buffer in file, up to pz 1.6
		self.index = 0

		# in bytes
		self.size = 0

		# id, new for pz 1.6
		self.file_hash = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 19:
			self.index = 0
		self.size = 0
		if self.context.version >= 20:
			self.file_hash = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		if instance.context.version <= 19:
			instance.index = stream.read_uint()
		instance.size = stream.read_uint()
		if instance.context.version >= 20:
			instance.file_hash = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		if instance.context.version <= 19:
			stream.write_uint(instance.index)
		stream.write_uint(instance.size)
		if instance.context.version >= 20:
			stream.write_uint(instance.file_hash)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'BufferEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* index = {fmt_member(self.index, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* file_hash = {fmt_member(self.file_hash, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	def read_data(self, stream):
		"""Load data from archive stream into self for modification and io"""
		self.data = stream.read(self.size)

	def update_data(self, data):
		"""Set data internal data so it can be written on save and update the size value"""
		self.data = data
		self.size = len(data)

	def __eq__(self, other):
		attr_check = ("index", "size", "file_hash")
		same = True
		for attr in attr_check:
			a = getattr(self, attr)
			b = getattr(other, attr)
			if a != b:
				logging.warning(f"Buffer differs for '{attr}' - {a} vs {b}")
				same = False
		return same

