import typing
from generated.array import Array
from generated.formats.ovl.compound.AssetEntry import AssetEntry
from generated.formats.ovl.compound.SetEntry import SetEntry


class SetHeader:

	"""
	defines amount of sets and assets
	(not a struct in barbasol)
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.set_count = 0
		self.asset_count = 0

		# must be 1065336831
		self.sig_a = 0

		# must be 16909320
		self.sig_b = 0
		self.sets = Array()
		self.assets = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.set_count = stream.read_uint()
		self.asset_count = stream.read_uint()
		self.sig_a = stream.read_uint()
		self.sig_b = stream.read_uint()
		self.sets.read(stream, SetEntry, self.set_count, None)
		self.assets.read(stream, AssetEntry, self.asset_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.set_count)
		stream.write_uint(self.asset_count)
		stream.write_uint(self.sig_a)
		stream.write_uint(self.sig_b)
		self.sets.write(stream, SetEntry, self.set_count, None)
		self.assets.write(stream, AssetEntry, self.asset_count, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'SetHeader [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* set_count = ' + self.set_count.__repr__()
		s += '\n	* asset_count = ' + self.asset_count.__repr__()
		s += '\n	* sig_a = ' + self.sig_a.__repr__()
		s += '\n	* sig_b = ' + self.sig_b.__repr__()
		s += '\n	* sets = ' + self.sets.__repr__()
		s += '\n	* assets = ' + self.assets.__repr__()
		s += '\n'
		return s
