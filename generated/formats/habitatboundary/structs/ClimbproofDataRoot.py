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

	_import_key = 'habitatboundary.structs.ClimbproofDataRoot'

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

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('climb_proof', Pointer, (0, ZString), (False, None), (None, None))
		yield ('climb_proof_cap_start', Pointer, (0, ZString), (False, None), (None, None))
		yield ('climb_proof_cap_end', Pointer, (0, ZString), (False, None), (None, None))
		yield ('climb_proof_bracket', Pointer, (0, ZString), (False, None), (None, None))
		yield ('post_gap', Float, (0, None), (False, None), (None, None))
		yield ('u_1', Float, (0, None), (False, 2.0), (None, None))
		yield ('zero', Uint64, (0, None), (True, 0), (None, None))

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
