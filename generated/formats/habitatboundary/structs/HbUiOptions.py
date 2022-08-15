from generated.formats.ovl_base.basic import Bool
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbUiOptions(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Controls the Straight-Curved option for barriers
		self.straight_curve = False

		# Controls the Windows option for barriers
		self.windows = False
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.straight_curve = False
		self.windows = False

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.straight_curve = Bool.from_stream(stream, instance.context, 0, None)
		instance.windows = Bool.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Bool.to_stream(stream, instance.straight_curve)
		Bool.to_stream(stream, instance.windows)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'straight_curve', Bool, (0, None), (False, None)
		yield 'windows', Bool, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'HbUiOptions [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* straight_curve = {self.fmt_member(self.straight_curve, indent+1)}'
		s += f'\n	* windows = {self.fmt_member(self.windows, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
