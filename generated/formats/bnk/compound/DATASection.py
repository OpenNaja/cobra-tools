import typing
from generated.array import Array


class DATASection:

	"""
	second Section of a soundback aux
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.wem_files_datas = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.wem_files_datas = stream.read_bytes((self.length))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_bytes(self.wem_files_datas)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'DATASection [Size: '+str(self.io_size)+', Address: '+str(self.io_start)+'] ' + self.name
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* wem_files_datas = ' + self.wem_files_datas.__repr__()
		s += '\n'
		return s
