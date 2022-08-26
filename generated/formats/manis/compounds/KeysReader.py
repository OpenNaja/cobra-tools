
import logging
import traceback

from generated.base_struct import BaseStruct
from generated.formats.manis.compounds.ManiBlock import ManiBlock
from modules.formats.shared import get_padding_size, get_padding


from generated.base_struct import BaseStruct


class KeysReader(BaseStruct):

	__name__ = 'KeysReader'

	_import_path = 'generated.formats.manis.compounds.KeysReader'

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
		yield from super()._get_filtered_attribute_list(instance)

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
			print(mani_info)
			print(stream.tell())
			mani_info.keys = ManiBlock.from_stream(stream, self.context, mani_info, None)
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

