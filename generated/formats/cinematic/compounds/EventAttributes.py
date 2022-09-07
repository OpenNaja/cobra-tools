from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class EventAttributes(MemStruct):

	"""
	24 bytes
	"""

	__name__ = 'EventAttributes'

	_import_path = 'generated.formats.cinematic.compounds.EventAttributes'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.anim_name = Pointer(self.context, 0, ZString)
		self.event_name = Pointer(self.context, 0, ZString)
		self.empty_string = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.anim_name = Pointer(self.context, 0, ZString)
		self.event_name = Pointer(self.context, 0, ZString)
		self.empty_string = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.anim_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.event_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.empty_string = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.anim_name, int):
			instance.anim_name.arg = 0
		if not isinstance(instance.event_name, int):
			instance.event_name.arg = 0
		if not isinstance(instance.empty_string, int):
			instance.empty_string.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.anim_name)
		Pointer.to_stream(stream, instance.event_name)
		Pointer.to_stream(stream, instance.empty_string)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'anim_name', Pointer, (0, ZString), (False, None)
		yield 'event_name', Pointer, (0, ZString), (False, None)
		yield 'empty_string', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'EventAttributes [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
