from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ButtonData(MemStruct):

	"""
	# Apparently the binding value is from a = 1..
	# HUD_MapMode:          13  209     m and M
	# HUD_Notifications:    14  210     n and N
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.k_1_a = 0
		self.k_1_b = 0
		self.k_2 = 0
		self.k_3 = 0
		self.k_4 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.k_1_a = 0
		self.k_1_b = 0
		self.k_2 = 0
		self.k_3 = 0
		self.k_4 = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.k_1_a = stream.read_ushort()
		instance.k_1_b = stream.read_ushort()
		instance.k_2 = stream.read_uint()
		instance.k_3 = stream.read_uint()
		instance.k_4 = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_ushort(instance.k_1_a)
		stream.write_ushort(instance.k_1_b)
		stream.write_uint(instance.k_2)
		stream.write_uint(instance.k_3)
		stream.write_uint(instance.k_4)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'k_1_a', Ushort, (0, None)
		yield 'k_1_b', Ushort, (0, None)
		yield 'k_2', Uint, (0, None)
		yield 'k_3', Uint, (0, None)
		yield 'k_4', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'ButtonData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* k_1_a = {self.fmt_member(self.k_1_a, indent+1)}'
		s += f'\n	* k_1_b = {self.fmt_member(self.k_1_b, indent+1)}'
		s += f'\n	* k_2 = {self.fmt_member(self.k_2, indent+1)}'
		s += f'\n	* k_3 = {self.fmt_member(self.k_3, indent+1)}'
		s += f'\n	* k_4 = {self.fmt_member(self.k_4, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
