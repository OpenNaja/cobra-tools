from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbPostSize(MemStruct):

	__name__ = 'HbPostSize'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Post size front and back. Affects navcut and selection.
		self.front_back = 0.0

		# Post size left and right. Affects navcut and selection.
		self.left_right = 0.0

		# Post size above wall. Affects navcut and selection.
		self.top = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.front_back = 0.0
		self.left_right = 0.0
		self.top = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.front_back = Float.from_stream(stream, instance.context, 0, None)
		instance.left_right = Float.from_stream(stream, instance.context, 0, None)
		instance.top = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.front_back)
		Float.to_stream(stream, instance.left_right)
		Float.to_stream(stream, instance.top)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'front_back', Float, (0, None), (False, None)
		yield 'left_right', Float, (0, None), (False, None)
		yield 'top', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'HbPostSize [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* front_back = {self.fmt_member(self.front_back, indent+1)}'
		s += f'\n	* left_right = {self.fmt_member(self.left_right, indent+1)}'
		s += f'\n	* top = {self.fmt_member(self.top, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
