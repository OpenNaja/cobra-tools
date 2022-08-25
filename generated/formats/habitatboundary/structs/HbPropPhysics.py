from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbPropPhysics(MemStruct):

	__name__ = 'HbPropPhysics'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Affects selection area above object.
		self.pad_top = 0.0

		# Z offset of box from prop object.
		self.z_pos = 0.0

		# Affects selection area and rejects barrier placement inside area.
		self.half_width = 0.0

		# Affects selection area below object.
		self.pad_bottom = 0.0

		# Affects selection area and rejects barrier placement inside area.
		self.half_depth = 0.0

		# Unknown effect. Possibly vertical offset of box, yet testing was inconclusive.
		self.u_6 = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.pad_top = 0.0
		self.z_pos = 0.0
		self.half_width = 0.0
		self.pad_bottom = 0.0
		self.half_depth = 0.0
		self.u_6 = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.pad_top = Float.from_stream(stream, instance.context, 0, None)
		instance.z_pos = Float.from_stream(stream, instance.context, 0, None)
		instance.half_width = Float.from_stream(stream, instance.context, 0, None)
		instance.pad_bottom = Float.from_stream(stream, instance.context, 0, None)
		instance.half_depth = Float.from_stream(stream, instance.context, 0, None)
		instance.u_6 = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.pad_top)
		Float.to_stream(stream, instance.z_pos)
		Float.to_stream(stream, instance.half_width)
		Float.to_stream(stream, instance.pad_bottom)
		Float.to_stream(stream, instance.half_depth)
		Float.to_stream(stream, instance.u_6)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'pad_top', Float, (0, None), (False, None)
		yield 'z_pos', Float, (0, None), (False, None)
		yield 'half_width', Float, (0, None), (False, None)
		yield 'pad_bottom', Float, (0, None), (False, None)
		yield 'half_depth', Float, (0, None), (False, None)
		yield 'u_6', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'HbPropPhysics [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* pad_top = {self.fmt_member(self.pad_top, indent+1)}'
		s += f'\n	* z_pos = {self.fmt_member(self.z_pos, indent+1)}'
		s += f'\n	* half_width = {self.fmt_member(self.half_width, indent+1)}'
		s += f'\n	* pad_bottom = {self.fmt_member(self.pad_bottom, indent+1)}'
		s += f'\n	* half_depth = {self.fmt_member(self.half_depth, indent+1)}'
		s += f'\n	* u_6 = {self.fmt_member(self.u_6, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
