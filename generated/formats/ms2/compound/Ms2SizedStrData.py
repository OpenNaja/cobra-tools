import typing
from generated.array import Array


class Ms2SizedStrData:

	"""
	Read at the entry point of the sized str entry for the ms2. Seems to be the 'root header' of the ms2.
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 32 if PC, 47 if JWE, 48 if PZ
		self.ms_2_version = 0

		# seems likely, 1 if yes, 0 if no
		self.has_model_data = 0

		# 3 in stairwell
		self.mdl_2_count = 0

		# count of names in ms2 buffer0
		self.name_count = 0

		# seems to be zeros
		self.unknown_1 = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.ms_2_version = stream.read_uint()
		stream.ms_2_version = self.ms_2_version
		self.has_model_data = stream.read_ushort()
		self.mdl_2_count = stream.read_ushort()
		self.name_count = stream.read_uint()
		self.unknown_1.read(stream, 'Uint', 3, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.ms_2_version)
		stream.ms_2_version = self.ms_2_version
		stream.write_ushort(self.has_model_data)
		stream.write_ushort(self.mdl_2_count)
		stream.write_uint(self.name_count)
		self.unknown_1.write(stream, 'Uint', 3, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Ms2SizedStrData [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* ms_2_version = ' + self.ms_2_version.__repr__()
		s += '\n	* has_model_data = ' + self.has_model_data.__repr__()
		s += '\n	* mdl_2_count = ' + self.mdl_2_count.__repr__()
		s += '\n	* name_count = ' + self.name_count.__repr__()
		s += '\n	* unknown_1 = ' + self.unknown_1.__repr__()
		s += '\n'
		return s
