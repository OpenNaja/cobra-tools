from source.formats.base.basic import fmt_member
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ovl.compound.AssetEntry import AssetEntry
from generated.formats.ovl.compound.SetEntry import SetEntry


class SetHeader:

	"""
	defines amount of sets and assets
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
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
		self.sets = Array((self.set_count,), SetEntry, self.context, 0, None)
		self.assets = Array((self.asset_count,), AssetEntry, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.set_count = 0
		self.asset_count = 0
		self.sig_a = 1065336831
		self.sig_b = 16909320
		self.sets = Array((self.set_count,), SetEntry, self.context, 0, None)
		self.assets = Array((self.asset_count,), AssetEntry, self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.set_count = stream.read_uint()
		instance.asset_count = stream.read_uint()
		instance.sig_a = stream.read_uint()
		instance.sig_b = stream.read_uint()
		instance.sets = Array.from_stream(stream, (instance.set_count,), SetEntry, instance.context, 0, None)
		instance.assets = Array.from_stream(stream, (instance.asset_count,), AssetEntry, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.set_count)
		stream.write_uint(instance.asset_count)
		stream.write_uint(instance.sig_a)
		stream.write_uint(instance.sig_b)
		Array.to_stream(stream, instance.sets, (instance.set_count,), SetEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.assets, (instance.asset_count,), AssetEntry, instance.context, 0, None)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'SetHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* set_count = {fmt_member(self.set_count, indent+1)}'
		s += f'\n	* asset_count = {fmt_member(self.asset_count, indent+1)}'
		s += f'\n	* sig_a = {fmt_member(self.sig_a, indent+1)}'
		s += f'\n	* sig_b = {fmt_member(self.sig_b, indent+1)}'
		s += f'\n	* sets = {fmt_member(self.sets, indent+1)}'
		s += f'\n	* assets = {fmt_member(self.assets, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
