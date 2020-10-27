import typing
from generated.array import Array
from generated.formats.bnk.compound.HircPointer import HircPointer


class HIRCSection:

	"""
	The HIRC section contains all the Wwise objects, including the events, the containers to group sounds, and the references to the sound files.
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.count = 0
		self.hirc_pointers = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.count = stream.read_uint()
		self.hirc_pointers.read(stream, HircPointer, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_uint(self.count)
		self.hirc_pointers.write(stream, HircPointer, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'HIRCSection [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* count = ' + self.count.__repr__()
		s += '\n	* hirc_pointers = ' + self.hirc_pointers.__repr__()
		s += '\n'
		return s
