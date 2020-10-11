import typing


class Ms2SizedStrData:

	"""
	Read at the entry point of the sized str entry for the ms2. Seems to be the 'root header' of the ms2.
	"""

	# 32 if PC, 47 if JWE, 48 if PZ
	ms_2_version: int

	# seems likely, 1 if yes, 0 if no
	has_model_data: int

	# 3 in stairwell
	mdl_2_count: int

	# count of names in ms2 buffer0
	name_count: int

	# seems to be zeros
	unknown_1: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.ms_2_version = 0
		self.has_model_data = 0
		self.mdl_2_count = 0
		self.name_count = 0
		self.unknown_1 = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.ms_2_version = stream.read_uint()
		stream.ms_2_version = self.ms_2_version
		self.has_model_data = stream.read_ushort()
		self.mdl_2_count = stream.read_ushort()
		self.name_count = stream.read_uint()
		self.unknown_1 = [stream.read_uint() for _ in range(3)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.ms_2_version)
		stream.ms_2_version = self.ms_2_version
		stream.write_ushort(self.has_model_data)
		stream.write_ushort(self.mdl_2_count)
		stream.write_uint(self.name_count)
		for item in self.unknown_1: stream.write_uint(item)

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
