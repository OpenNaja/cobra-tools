import generated.formats.base.basic
import generated.formats.motiongraph.compounds.ActivitiesLinks
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.motiongraph.enums.SelectActivityActivityMode import SelectActivityActivityMode
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SelectActivityActivityData(MemStruct):

	"""
	32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_activities = 0
		self.blend_time = 0.0
		self.mode = SelectActivityActivityMode(self.context, 0, None)
		self.enum_variable = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.activities = Pointer(self.context, self.num_activities, generated.formats.motiongraph.compounds.ActivitiesLinks.ActivitiesLinks)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.num_activities = 0
		self.blend_time = 0.0
		self.mode = SelectActivityActivityMode(self.context, 0, None)
		self.enum_variable = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.activities = Pointer(self.context, self.num_activities, generated.formats.motiongraph.compounds.ActivitiesLinks.ActivitiesLinks)

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
		instance.enum_variable = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.activities = Pointer.from_stream(stream, instance.context, instance.num_activities, generated.formats.motiongraph.compounds.ActivitiesLinks.ActivitiesLinks)
		instance.num_activities = stream.read_uint64()
		instance.blend_time = stream.read_float()
		instance.mode = SelectActivityActivityMode.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.enum_variable, int):
			instance.enum_variable.arg = 0
		if not isinstance(instance.activities, int):
			instance.activities.arg = instance.num_activities

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.enum_variable)
		Pointer.to_stream(stream, instance.activities)
		stream.write_uint64(instance.num_activities)
		stream.write_float(instance.blend_time)
		SelectActivityActivityMode.to_stream(stream, instance.mode)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('enum_variable', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('activities', Pointer, (instance.num_activities, generated.formats.motiongraph.compounds.ActivitiesLinks.ActivitiesLinks))
		yield ('num_activities', Uint64, (0, None))
		yield ('blend_time', Float, (0, None))
		yield ('mode', SelectActivityActivityMode, (0, None))

	def get_info_str(self, indent=0):
		return f'SelectActivityActivityData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* enum_variable = {self.fmt_member(self.enum_variable, indent+1)}'
		s += f'\n	* activities = {self.fmt_member(self.activities, indent+1)}'
		s += f'\n	* num_activities = {self.fmt_member(self.num_activities, indent+1)}'
		s += f'\n	* blend_time = {self.fmt_member(self.blend_time, indent+1)}'
		s += f'\n	* mode = {self.fmt_member(self.mode, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
