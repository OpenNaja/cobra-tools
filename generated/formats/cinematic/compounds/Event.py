from generated.formats.base.basic import Float
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Event(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'Event'

	_import_path = 'generated.formats.cinematic.compounds.Event'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.start_time = 0.0
		self.b = 0.0
		self.duration = 0.0
		self.d = 0.0
		self.module_name = Pointer(self.context, 0, ZString)
		self.attributes = Pointer(self.context, 0, Event._import_path_map["generated.formats.cinematic.compounds.EventAttributes"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.start_time = 0.0
		self.b = 0.0
		self.duration = 0.0
		self.d = 0.0
		self.module_name = Pointer(self.context, 0, ZString)
		self.attributes = Pointer(self.context, 0, Event._import_path_map["generated.formats.cinematic.compounds.EventAttributes"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.start_time = Float.from_stream(stream, instance.context, 0, None)
		instance.b = Float.from_stream(stream, instance.context, 0, None)
		instance.module_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.attributes = Pointer.from_stream(stream, instance.context, 0, Event._import_path_map["generated.formats.cinematic.compounds.EventAttributes"])
		instance.duration = Float.from_stream(stream, instance.context, 0, None)
		instance.d = Float.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.module_name, int):
			instance.module_name.arg = 0
		if not isinstance(instance.attributes, int):
			instance.attributes.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.start_time)
		Float.to_stream(stream, instance.b)
		Pointer.to_stream(stream, instance.module_name)
		Pointer.to_stream(stream, instance.attributes)
		Float.to_stream(stream, instance.duration)
		Float.to_stream(stream, instance.d)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'start_time', Float, (0, None), (False, None)
		yield 'b', Float, (0, None), (False, None)
		yield 'module_name', Pointer, (0, ZString), (False, None)
		yield 'attributes', Pointer, (0, Event._import_path_map["generated.formats.cinematic.compounds.EventAttributes"]), (False, None)
		yield 'duration', Float, (0, None), (False, None)
		yield 'd', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Event [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
