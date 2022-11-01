from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ms2.compounds.AxisAngle import AxisAngle
from generated.formats.ms2.compounds.Vector3 import Vector3


class TriChunk(BaseStruct):

	"""
	JWE2 Biosyn: 64 bytes
	"""

	__name__ = 'TriChunk'

	_import_key = 'ms2.compounds.TriChunk'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# the smallest coordinates across all axes, min of unpacked vert coords if loc is 0,0,0
		self.bounds_min = Vector3(self.context, 0, None)
		self.material_index = 0
		self.tris_count = 0

		# the biggest coordinates across all axes, max of unpacked vert coords if loc is 0,0,0
		self.bounds_max = Vector3(self.context, 0, None)
		self.tris_offset = 0

		# can be 0,0,0, no obvious range, not always within range of bounds
		self.loc = Vector3(self.context, 0, None)

		# can be 1, 0, 0, 0; w always in range -1, +1
		self.rot = AxisAngle(self.context, 0, None)
		self.shell_index = 0
		self.shell_count = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('bounds_min', Vector3, (0, None), (False, None), None),
		('material_index', Ushort, (0, None), (False, None), None),
		('tris_count', Ushort, (0, None), (False, None), None),
		('bounds_max', Vector3, (0, None), (False, None), None),
		('tris_offset', Uint, (0, None), (False, None), None),
		('loc', Vector3, (0, None), (False, None), None),
		('rot', AxisAngle, (0, None), (False, None), None),
		('shell_index', Ushort, (0, None), (False, None), None),
		('shell_count', Ushort, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'bounds_min', Vector3, (0, None), (False, None)
		yield 'material_index', Ushort, (0, None), (False, None)
		yield 'tris_count', Ushort, (0, None), (False, None)
		yield 'bounds_max', Vector3, (0, None), (False, None)
		yield 'tris_offset', Uint, (0, None), (False, None)
		yield 'loc', Vector3, (0, None), (False, None)
		yield 'rot', AxisAngle, (0, None), (False, None)
		yield 'shell_index', Ushort, (0, None), (False, None)
		yield 'shell_count', Ushort, (0, None), (False, None)
