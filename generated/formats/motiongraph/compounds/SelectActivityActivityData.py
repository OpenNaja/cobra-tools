from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.enums.SelectActivityActivityMode import SelectActivityActivityMode
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SelectActivityActivityData(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'SelectActivityActivityData'

	_import_key = 'motiongraph.compounds.SelectActivityActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_activities = 0
		self.blend_time = 0.0
		self.mode = SelectActivityActivityMode(self.context, 0, None)
		self.enum_variable = Pointer(self.context, 0, ZString)
		self.activities = Pointer(self.context, self.num_activities, SelectActivityActivityData._import_map["motiongraph.compounds.ActivitiesLinks"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'enum_variable', Pointer, (0, ZString), (False, None)
		yield 'activities', Pointer, (instance.num_activities, SelectActivityActivityData._import_map["motiongraph.compounds.ActivitiesLinks"]), (False, None)
		yield 'num_activities', Uint64, (0, None), (False, None)
		yield 'blend_time', Float, (0, None), (False, None)
		yield 'mode', SelectActivityActivityMode, (0, None), (False, None)
