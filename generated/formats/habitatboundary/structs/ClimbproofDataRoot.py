from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ClimbproofDataRoot(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'ClimbproofDataRoot'

	_import_path = 'generated.formats.habitatboundary.structs.ClimbproofDataRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Distance between post center and start of bracket.
		self.post_gap = 0.0
		self.u_1 = 2.0
		self.zero = 0
		self.climb_proof = Pointer(self.context, 0, ZString)
		self.climb_proof_cap_start = Pointer(self.context, 0, ZString)
		self.climb_proof_cap_end = Pointer(self.context, 0, ZString)
		self.climb_proof_bracket = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.post_gap = 0.0
		self.u_1 = 2.0
		self.zero = 0
		self.climb_proof = Pointer(self.context, 0, ZString)
		self.climb_proof_cap_start = Pointer(self.context, 0, ZString)
		self.climb_proof_cap_end = Pointer(self.context, 0, ZString)
		self.climb_proof_bracket = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.climb_proof = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.climb_proof_cap_start = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.climb_proof_cap_end = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.climb_proof_bracket = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.post_gap = Float.from_stream(stream, instance.context, 0, None)
		instance.u_1 = Float.from_stream(stream, instance.context, 0, None)
		instance.zero = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.climb_proof, int):
			instance.climb_proof.arg = 0
		if not isinstance(instance.climb_proof_cap_start, int):
			instance.climb_proof_cap_start.arg = 0
		if not isinstance(instance.climb_proof_cap_end, int):
			instance.climb_proof_cap_end.arg = 0
		if not isinstance(instance.climb_proof_bracket, int):
			instance.climb_proof_bracket.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.climb_proof)
		Pointer.to_stream(stream, instance.climb_proof_cap_start)
		Pointer.to_stream(stream, instance.climb_proof_cap_end)
		Pointer.to_stream(stream, instance.climb_proof_bracket)
		Float.to_stream(stream, instance.post_gap)
		Float.to_stream(stream, instance.u_1)
		Uint64.to_stream(stream, instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'climb_proof', Pointer, (0, ZString), (False, None)
		yield 'climb_proof_cap_start', Pointer, (0, ZString), (False, None)
		yield 'climb_proof_cap_end', Pointer, (0, ZString), (False, None)
		yield 'climb_proof_bracket', Pointer, (0, ZString), (False, None)
		yield 'post_gap', Float, (0, None), (False, None)
		yield 'u_1', Float, (0, None), (False, 2.0)
		yield 'zero', Uint64, (0, None), (True, 0)

	def get_info_str(self, indent=0):
		return f'ClimbproofDataRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
