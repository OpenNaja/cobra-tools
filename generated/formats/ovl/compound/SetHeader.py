import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ovl.compound.AssetEntry import AssetEntry
from generated.formats.ovl.compound.SetEntry import SetEntry


class SetHeader:

	"""
	defines amount of sets and assets
	(not a struct in barbasol)
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.set_count = 0
		self.asset_count = 0

		# must be 1065336831
		self.sig_a = 1065336831

		# must be 16909320
		self.sig_b = 16909320
		self.sets = Array(self.context)
		self.assets = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.set_count = 0
		self.asset_count = 0
		self.sig_a = 1065336831
		self.sig_b = 16909320
		self.sets = Array(self.context)
		self.assets = Array(self.context)

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

	def get_info_str(self):
		return f'SetHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* set_count = {self.set_count.__repr__()}'
		s += f'\n	* asset_count = {self.asset_count.__repr__()}'
		s += f'\n	* sig_a = {self.sig_a.__repr__()}'
		s += f'\n	* sig_b = {self.sig_b.__repr__()}'
		s += f'\n	* sets = {self.sets.__repr__()}'
		s += f'\n	* assets = {self.assets.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
