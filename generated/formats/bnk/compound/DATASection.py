import typing


class DATASection:

	"""
	second Section of a soundback aux
	"""

	# length of following data
	length: int
	wem_files_datas: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.length = 0
		self.wem_files_datas = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.wem_files_datas = [stream.read_byte() for _ in range(self.length)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		for item in self.wem_files_datas: stream.write_byte(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'DATASection [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* wem_files_datas = ' + self.wem_files_datas.__repr__()
		s += '\n'
		return s
