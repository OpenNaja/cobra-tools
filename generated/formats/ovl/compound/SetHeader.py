import typing
from generated.formats.ovl.compound.AssetEntry import AssetEntry
from generated.formats.ovl.compound.SetEntry import SetEntry


class SetHeader:

	"""
	defines amount of sets and assets
	(not a struct in barbasol)
	"""
	set_count: int
	asset_count: int

	# must be 1065336831
	sig_a: int

	# must be 16909320
	sig_b: int
	sets: typing.List[SetEntry]
	assets: typing.List[AssetEntry]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.set_count = 0
		self.asset_count = 0
		self.sig_a = 0
		self.sig_b = 0
		self.sets = []
		self.assets = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.set_count = stream.read_uint()
		self.asset_count = stream.read_uint()
		self.sig_a = stream.read_uint()
		self.sig_b = stream.read_uint()
		self.sets = [stream.read_type(SetEntry) for _ in range(self.set_count)]
		self.assets = [stream.read_type(AssetEntry) for _ in range(self.asset_count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.set_count)
		stream.write_uint(self.asset_count)
		stream.write_uint(self.sig_a)
		stream.write_uint(self.sig_b)
		for item in self.sets: stream.write_type(item)
		for item in self.assets: stream.write_type(item)

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
