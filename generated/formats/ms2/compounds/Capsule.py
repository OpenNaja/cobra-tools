from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ms2.compounds.Vector3 import Vector3


class Capsule(BaseStruct):

	__name__ = 'Capsule'

	_import_path = 'generated.formats.ms2.compounds.Capsule'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# relative to the armature, ie. not in bone space
		self.offset = Vector3(self.context, 0, None)

		# normalized
		self.direction = Vector3(self.context, 0, None)

		# radius of the caps
		self.radius = 0.0

		# distance between the center points of the capsule caps, total extent is 2 * radius + extent
		self.extent = 0.0

		# apparently unused
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.offset = Vector3(self.context, 0, None)
		self.direction = Vector3(self.context, 0, None)
		self.radius = 0.0
		self.extent = 0.0
		self.zero = 0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', Vector3, (0, None), (False, None)
		yield 'direction', Vector3, (0, None), (False, None)
		yield 'radius', Float, (0, None), (False, None)
		yield 'extent', Float, (0, None), (False, None)
		yield 'zero', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Capsule [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
