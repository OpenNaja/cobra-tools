from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo


class Mdl2Descriptor(CoreModelInfo):

	"""
	Wraps a CoreModelInfo
	"""

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.materials_ptr = 0
		self.lods_ptr = 0
		self.objects_ptr = 0
		self.models_ptr = 0
		self.first_materials_ptr = 0

		# unknown, probably used to increment skeleton
		self.increment_flag = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.set_defaults()

	def set_defaults(self):
		self.materials_ptr = 0
		self.lods_ptr = 0
		self.objects_ptr = 0
		self.models_ptr = 0
		self.first_materials_ptr = 0
		self.increment_flag = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.materials_ptr = stream.read_uint64()
		self.lods_ptr = stream.read_uint64()
		self.objects_ptr = stream.read_uint64()
		self.models_ptr = stream.read_uint64()
		self.first_materials_ptr = stream.read_uint64()
		self.increment_flag = stream.read_uint64()
		self.zero_0 = stream.read_uint64()
		self.zero_1 = stream.read_uint64()
		self.zero_2 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_uint64(self.materials_ptr)
		stream.write_uint64(self.lods_ptr)
		stream.write_uint64(self.objects_ptr)
		stream.write_uint64(self.models_ptr)
		stream.write_uint64(self.first_materials_ptr)
		stream.write_uint64(self.increment_flag)
		stream.write_uint64(self.zero_0)
		stream.write_uint64(self.zero_1)
		stream.write_uint64(self.zero_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Mdl2Descriptor [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* materials_ptr = {self.materials_ptr.__repr__()}'
		s += f'\n	* lods_ptr = {self.lods_ptr.__repr__()}'
		s += f'\n	* objects_ptr = {self.objects_ptr.__repr__()}'
		s += f'\n	* models_ptr = {self.models_ptr.__repr__()}'
		s += f'\n	* first_materials_ptr = {self.first_materials_ptr.__repr__()}'
		s += f'\n	* increment_flag = {self.increment_flag.__repr__()}'
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
