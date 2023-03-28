from generated.formats.base.basic import Float
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Event(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'Event'

	_import_key = 'cinematic.compounds.Event'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.start_time = 0.0
		self.b = 0.0
		self.duration = 0.0
		self.d = 0.0
		self.module_name = Pointer(self.context, 0, ZString)
		self.attributes = Pointer(self.context, 0, Event._import_map["cinematic.compounds.EventAttributes"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('start_time', Float, (0, None), (False, None), None)
		yield ('b', Float, (0, None), (False, None), None)
		yield ('module_name', Pointer, (0, ZString), (False, None), None)
		yield ('attributes', Pointer, (0, Event._import_map["cinematic.compounds.EventAttributes"]), (False, None), None)
		yield ('duration', Float, (0, None), (False, None), None)
		yield ('d', Float, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'start_time', Float, (0, None), (False, None)
		yield 'b', Float, (0, None), (False, None)
		yield 'module_name', Pointer, (0, ZString), (False, None)
		yield 'attributes', Pointer, (0, Event._import_map["cinematic.compounds.EventAttributes"]), (False, None)
		yield 'duration', Float, (0, None), (False, None)
		yield 'd', Float, (0, None), (False, None)


Event.init_attributes()
