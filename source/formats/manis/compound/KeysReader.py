# START_GLOBALS
import logging
import traceback

from generated.context import ContextReference
from generated.formats.manis.compound import ManiBlock
from modules.formats.shared import get_padding_size, get_padding


# END_GLOBALS


class KeysReader:

	context = ContextReference()

	# START_CLASS

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.bone_infos = []
		self.set_defaults()
		self.bone_info_start = 0

	def set_defaults(self):
		pass

	def read(self, stream):
		self.io_start = stream.tell()
		for mani_info in self.arg:
			mani_info.keys = stream.read_type(ManiBlock, (self.context, mani_info,))
			print(mani_info)
			print(mani_info.keys)

			sum_bytes = sum(mb.byte_size for mb in mani_info.keys.repeats)
			print("sum_bytes", sum_bytes)
			sum_bytes2 = sum(mb.byte_size + get_padding_size(mb.byte_size) for mb in mani_info.keys.repeats)
			print("sum_bytes + padding", sum_bytes2)
			for mb in mani_info.keys.repeats:
				# print(bone_name, stream.tell())
				mb.data = stream.read(mb.byte_size)
				pad_size = get_padding_size(mb.byte_size)
				mb.padding = stream.read(pad_size)
				# print("end", stream.tell())
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		for mani_info in self.arg:
			mani_info.keys.write(stream)
			for mb in mani_info.keys.repeats:
				stream.write(mb.data)
				stream.write(get_padding(mb.byte_size))
		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Model [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		for mani_info in self.arg:
			s += str(mani_info.keys)
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
