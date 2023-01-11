from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.ms2.bitfields.WeightsFlag import WeightsFlag
from generated.formats.ms2.bitfields.WeightsFlagMalta import WeightsFlagMalta


class VertChunk(BaseStruct):

	"""
	JWE2 Biosyn: 16 bytes
	"""

	__name__ = 'VertChunk'

	_import_key = 'ms2.compounds.VertChunk'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# apparently also used for scaling the mesh: pack_base / 512 / 2048 = scale
		self.scale = 0.0

		# the usual mesh scale: pack_base / 512, also added as offset during vertex packing
		self.pack_base = 0.0

		# byte offset from start of vert buffer in bytes
		self.vertex_offset = 0
		self.vertex_count = 0

		# determines if weights are used by this chunk
		self.weights_flag = WeightsFlagMalta(self.context, 0, None)
		self.zero = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('scale', Float, (0, None), (False, None), None),
		('pack_base', Float, (0, None), (False, None), None),
		('vertex_offset', Uint, (0, None), (False, None), None),
		('vertex_count', Ubyte, (0, None), (False, None), None),
		('weights_flag', WeightsFlag, (0, None), (False, None), True),
		('weights_flag', WeightsFlagMalta, (0, None), (False, None), True),
		('zero', Ubyte, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'scale', Float, (0, None), (False, None)
		yield 'pack_base', Float, (0, None), (False, None)
		yield 'vertex_offset', Uint, (0, None), (False, None)
		yield 'vertex_count', Ubyte, (0, None), (False, None)
		if instance.context.version <= 51:
			yield 'weights_flag', WeightsFlag, (0, None), (False, None)
		if instance.context.version >= 52:
			yield 'weights_flag', WeightsFlagMalta, (0, None), (False, None)
		yield 'zero', Ubyte, (0, None), (False, None)
