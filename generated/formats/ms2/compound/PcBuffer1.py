from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.CoreModelInfoPC import CoreModelInfoPC
from generated.formats.ms2.compound.Ms2BufferInfoPC import Ms2BufferInfoPC
from generated.formats.ms2.compound.Ms2BufferInfoZT import Ms2BufferInfoZT


class PcBuffer1:

	"""
	cond="general info \ ms2 version == 32"
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.buffer_info_pc = Ms2BufferInfoZT(self.context, self.arg, None)
		self.buffer_info_pc = Ms2BufferInfoPC(self.context, 0, None)
		self.model_infos = Array((self.arg.general_info.mdl_2_count,), CoreModelInfoPC, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version == 17:
			self.buffer_info_pc = Ms2BufferInfoZT(self.context, self.arg, None)
		if self.context.version == 18:
			self.buffer_info_pc = Ms2BufferInfoPC(self.context, 0, None)
		self.model_infos = Array((self.arg.general_info.mdl_2_count,), CoreModelInfoPC, self.context, 0, None)

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
		if instance.context.version == 17:
			instance.buffer_info_pc = Ms2BufferInfoZT.from_stream(stream, instance.context, instance.arg, None)
		if instance.context.version == 18:
			instance.buffer_info_pc = Ms2BufferInfoPC.from_stream(stream, instance.context, 0, None)
		instance.model_infos = Array.from_stream(stream, (instance.arg.general_info.mdl_2_count,), CoreModelInfoPC, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		if instance.context.version == 17:
			Ms2BufferInfoZT.to_stream(stream, instance.buffer_info_pc)
		if instance.context.version == 18:
			Ms2BufferInfoPC.to_stream(stream, instance.buffer_info_pc)
		Array.to_stream(stream, instance.model_infos, (instance.arg.general_info.mdl_2_count,), CoreModelInfoPC, instance.context, 0, None)

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

	def get_info_str(self):
		return f'PcBuffer1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* buffer_info_pc = {self.buffer_info_pc.__repr__()}'
		s += f'\n	* model_infos = {self.model_infos.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
