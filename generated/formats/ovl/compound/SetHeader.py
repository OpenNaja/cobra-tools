from generated.formats.ovl.compound.SetEntry import SetEntry
import typing
from generated.formats.ovl.compound.AssetEntry import AssetEntry


class SetHeader:

# defines amount of sets and assets
# (not a struct in barbasol)
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

	def read(self, stream):
		self.set_count = stream.read_uint()
		self.asset_count = stream.read_uint()
		self.sig_a = stream.read_uint()
		self.sig_b = stream.read_uint()
		self.sets = [stream.read_type(SetEntry) for _ in range(self.set_count)]
		self.assets = [stream.read_type(AssetEntry) for _ in range(self.asset_count)]

	def write(self, stream):
		stream.write_uint(self.set_count)
		stream.write_uint(self.asset_count)
		stream.write_uint(self.sig_a)
		stream.write_uint(self.sig_b)
		for item in self.sets: stream.write_type(item)
		for item in self.assets: stream.write_type(item)

	def __repr__(self):
		s = 'SetHeader'
		s += '\nset_count ' + self.set_count.__repr__()
		s += '\nasset_count ' + self.asset_count.__repr__()
		s += '\nsig_a ' + self.sig_a.__repr__()
		s += '\nsig_b ' + self.sig_b.__repr__()
		s += '\nsets ' + self.sets.__repr__()
		s += '\nassets ' + self.assets.__repr__()
		s += '\n'
		return s