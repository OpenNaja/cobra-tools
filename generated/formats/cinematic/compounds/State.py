from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class State(MemStruct):

	"""
	JWE2: 64 bytes
	"""

	__name__ = 'State'

	_import_key = 'cinematic.compounds.State'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.abstract_name = Pointer(self.context, 0, ZString)
		self.concrete_name = Pointer(self.context, 0, ZString)
		self.debug_name = Pointer(self.context, 0, ZString)
		self.events_list = Pointer(self.context, 0, State._import_map["cinematic.compounds.EventsList"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('abstract_name', Pointer, (0, ZString), (False, None), None),
		('concrete_name', Pointer, (0, ZString), (False, None), None),
		('debug_name', Pointer, (0, ZString), (False, None), None),
		('a', Uint64, (0, None), (False, None), None),
		('b', Uint64, (0, None), (False, None), None),
		('c', Uint64, (0, None), (False, None), None),
		('events_list', Pointer, (0, None), (False, None), None),
		('d', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'abstract_name', Pointer, (0, ZString), (False, None)
		yield 'concrete_name', Pointer, (0, ZString), (False, None)
		yield 'debug_name', Pointer, (0, ZString), (False, None)
		yield 'a', Uint64, (0, None), (False, None)
		yield 'b', Uint64, (0, None), (False, None)
		yield 'c', Uint64, (0, None), (False, None)
		yield 'events_list', Pointer, (0, State._import_map["cinematic.compounds.EventsList"]), (False, None)
		yield 'd', Uint64, (0, None), (False, None)
