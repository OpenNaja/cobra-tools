from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class ClimbproofDataRoot(MemStruct):

	"""
	48 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Distance between post center and start of bracket.
		self.post_gap = 0.0
		self.u_1 = 0.0
		self.zero = 0
		self.climb_proof = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.climb_proof_cap_start = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.climb_proof_cap_end = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.climb_proof_bracket = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.post_gap = 0.0
		self.u_1 = 0.0
		self.zero = 0
		self.climb_proof = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.climb_proof_cap_start = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.climb_proof_cap_end = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.climb_proof_bracket = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		super().read_fields(stream, instance)
		instance.climb_proof = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.climb_proof_cap_start = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.climb_proof_cap_end = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.climb_proof_bracket = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.post_gap = stream.read_float()
		instance.u_1 = stream.read_float()
		instance.zero = stream.read_uint64()
		instance.climb_proof.arg = 0
		instance.climb_proof_cap_start.arg = 0
		instance.climb_proof_cap_end.arg = 0
		instance.climb_proof_bracket.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.climb_proof)
		Pointer.to_stream(stream, instance.climb_proof_cap_start)
		Pointer.to_stream(stream, instance.climb_proof_cap_end)
		Pointer.to_stream(stream, instance.climb_proof_bracket)
		stream.write_float(instance.post_gap)
		stream.write_float(instance.u_1)
		stream.write_uint64(instance.zero)

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
		return f'ClimbproofDataRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* climb_proof = {fmt_member(self.climb_proof, indent+1)}'
		s += f'\n	* climb_proof_cap_start = {fmt_member(self.climb_proof_cap_start, indent+1)}'
		s += f'\n	* climb_proof_cap_end = {fmt_member(self.climb_proof_cap_end, indent+1)}'
		s += f'\n	* climb_proof_bracket = {fmt_member(self.climb_proof_bracket, indent+1)}'
		s += f'\n	* post_gap = {fmt_member(self.post_gap, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
