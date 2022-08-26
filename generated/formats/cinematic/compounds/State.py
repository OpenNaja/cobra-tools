from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class State(MemStruct):

	"""
	JWE2: 64 bytes
	"""

	__name__ = 'State'

	_import_path = 'generated.formats.cinematic.compounds.State'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.abstract_name = Pointer(self.context, 0, ZString)
		self.concrete_name = Pointer(self.context, 0, ZString)
		self.debug_name = Pointer(self.context, 0, ZString)
		self.events_list = Pointer(self.context, 0, State._import_path_map["generated.formats.cinematic.compounds.EventsList"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.abstract_name = Pointer(self.context, 0, ZString)
		self.concrete_name = Pointer(self.context, 0, ZString)
		self.debug_name = Pointer(self.context, 0, ZString)
		self.events_list = Pointer(self.context, 0, State._import_path_map["generated.formats.cinematic.compounds.EventsList"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.abstract_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.concrete_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.debug_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.a = Uint64.from_stream(stream, instance.context, 0, None)
		instance.b = Uint64.from_stream(stream, instance.context, 0, None)
		instance.c = Uint64.from_stream(stream, instance.context, 0, None)
		instance.events_list = Pointer.from_stream(stream, instance.context, 0, State._import_path_map["generated.formats.cinematic.compounds.EventsList"])
		instance.d = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.abstract_name, int):
			instance.abstract_name.arg = 0
		if not isinstance(instance.concrete_name, int):
			instance.concrete_name.arg = 0
		if not isinstance(instance.debug_name, int):
			instance.debug_name.arg = 0
		if not isinstance(instance.events_list, int):
			instance.events_list.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.abstract_name)
		Pointer.to_stream(stream, instance.concrete_name)
		Pointer.to_stream(stream, instance.debug_name)
		Uint64.to_stream(stream, instance.a)
		Uint64.to_stream(stream, instance.b)
		Uint64.to_stream(stream, instance.c)
		Pointer.to_stream(stream, instance.events_list)
		Uint64.to_stream(stream, instance.d)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'abstract_name', Pointer, (0, ZString), (False, None)
		yield 'concrete_name', Pointer, (0, ZString), (False, None)
		yield 'debug_name', Pointer, (0, ZString), (False, None)
		yield 'a', Uint64, (0, None), (False, None)
		yield 'b', Uint64, (0, None), (False, None)
		yield 'c', Uint64, (0, None), (False, None)
		yield 'events_list', Pointer, (0, State._import_path_map["generated.formats.cinematic.compounds.EventsList"]), (False, None)
		yield 'd', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'State [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* abstract_name = {self.fmt_member(self.abstract_name, indent+1)}'
		s += f'\n	* concrete_name = {self.fmt_member(self.concrete_name, indent+1)}'
		s += f'\n	* debug_name = {self.fmt_member(self.debug_name, indent+1)}'
		s += f'\n	* a = {self.fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {self.fmt_member(self.b, indent+1)}'
		s += f'\n	* c = {self.fmt_member(self.c, indent+1)}'
		s += f'\n	* events_list = {self.fmt_member(self.events_list, indent+1)}'
		s += f'\n	* d = {self.fmt_member(self.d, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
