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

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'anim_name', Pointer, (0, ZString), (False, None)
		yield 'event_name', Pointer, (0, ZString), (False, None)
		yield 'empty_string', Pointer, (0, ZString), (False, None)
