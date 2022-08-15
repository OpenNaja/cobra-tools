import generated.formats.base.basic
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.motiongraph.enums.SelectActivityActivityMode import SelectActivityActivityMode
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RandomActivityActivityInfoData(MemStruct):

	"""
	bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.activities_count = 0
		self.blend_time = 0.0
		self.mode = SelectActivityActivityMode(self.context, 0, None)
		self.enum_variable = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.activities = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.activities_count = 0
		self.blend_time = 0.0
		self.mode = SelectActivityActivityMode(self.context, 0, None)
		self.enum_variable = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.activities = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.enum_variable = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.activities = Pointer.from_stream(stream, instance.context, 0, None)
		instance.activities_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.blend_time = Float.from_stream(stream, instance.context, 0, None)
		instance.mode = SelectActivityActivityMode.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.enum_variable, int):
			instance.enum_variable.arg = 0
		if not isinstance(instance.activities, int):
			instance.activities.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.enum_variable)
		Pointer.to_stream(stream, instance.activities)
		stream.write_uint64(instance.activities_count)
		stream.write_float(instance.blend_time)
		SelectActivityActivityMode.to_stream(stream, instance.mode)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'enum_variable', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'activities', Pointer, (0, None)
		yield 'activities_count', Uint64, (0, None)
		yield 'blend_time', Float, (0, None)
		yield 'mode', SelectActivityActivityMode, (0, None)

	def get_info_str(self, indent=0):
		return f'RandomActivityActivityInfoData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* enum_variable = {self.fmt_member(self.enum_variable, indent+1)}'
		s += f'\n	* activities = {self.fmt_member(self.activities, indent+1)}'
		s += f'\n	* activities_count = {self.fmt_member(self.activities_count, indent+1)}'
		s += f'\n	* blend_time = {self.fmt_member(self.blend_time, indent+1)}'
		s += f'\n	* mode = {self.fmt_member(self.mode, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
