from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbDoorCutout(MemStruct):

	"""
	Positions to create door cutout in a wall.
	"""

	__name__ = 'HbDoorCutout'

	_import_path = 'generated.formats.habitatboundary.structs.HbDoorCutout'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Wall cutout height for door.
		self.height = 0.0

		# Wall cutout position for right of door.
		self.right = 0.0

		# Wall cutout position for left of door.
		self.left = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.height = 0.0
		self.right = 0.0
		self.left = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.height = Float.from_stream(stream, instance.context, 0, None)
		instance.right = Float.from_stream(stream, instance.context, 0, None)
		instance.left = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.height)
		Float.to_stream(stream, instance.right)
		Float.to_stream(stream, instance.left)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'height', Float, (0, None), (False, None)
		yield 'right', Float, (0, None), (False, None)
		yield 'left', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'HbDoorCutout [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* height = {self.fmt_member(self.height, indent+1)}'
		s += f'\n	* right = {self.fmt_member(self.right, indent+1)}'
		s += f'\n	* left = {self.fmt_member(self.left, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
