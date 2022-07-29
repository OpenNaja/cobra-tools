from generated.formats.base.basic import fmt_member
from generated.formats.motiongraph.compound.FloatInputData import FloatInputData
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class FootPlantActivityData(MemStruct):

	"""
	48 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.weight = 0
		self.rotation_no_i_k_weight = 0
		self.sticky_feet_weight = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.weight = FloatInputData(self.context, 0, None)
		self.rotation_no_i_k_weight = FloatInputData(self.context, 0, None)
		self.sticky_feet_weight = FloatInputData(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.weight = FloatInputData.from_stream(stream, instance.context, 0, None)
		instance.rotation_no_i_k_weight = FloatInputData.from_stream(stream, instance.context, 0, None)
		instance.sticky_feet_weight = FloatInputData.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		FloatInputData.to_stream(stream, instance.weight)
		FloatInputData.to_stream(stream, instance.rotation_no_i_k_weight)
		FloatInputData.to_stream(stream, instance.sticky_feet_weight)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('weight', FloatInputData, (0, None))
		yield ('rotation_no_i_k_weight', FloatInputData, (0, None))
		yield ('sticky_feet_weight', FloatInputData, (0, None))

	def get_info_str(self, indent=0):
		return f'FootPlantActivityData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* weight = {fmt_member(self.weight, indent+1)}'
		s += f'\n	* rotation_no_i_k_weight = {fmt_member(self.rotation_no_i_k_weight, indent+1)}'
		s += f'\n	* sticky_feet_weight = {fmt_member(self.sticky_feet_weight, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
