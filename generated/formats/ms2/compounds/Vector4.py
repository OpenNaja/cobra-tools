from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class Vector4(BaseStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	__name__ = 'Vector4'

	_import_path = 'generated.formats.ms2.compounds.Vector4'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# First coordinate.
		self.x = 0.0

		# Second coordinate.
		self.y = 0.0

		# Third coordinate.
		self.z = 0.0

		# zeroth coordinate.
		self.w = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', Float, (0, None), (False, None)
		yield 'y', Float, (0, None), (False, None)
		yield 'z', Float, (0, None), (False, None)
		yield 'w', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Vector4 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def __repr__(self):
		return f"[ {self.x:6.3f} {self.y:6.3f} {self.z:6.3f} {self.w:6.3f} ]"

