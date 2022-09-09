from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbPropPhysics(MemStruct):

	__name__ = 'HB_PropPhysics'

	_import_key = 'habitatboundary.structs.HbPropPhysics'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Affects selection area above object.
		self.pad_top = 0.0

		# Z offset of box from prop object.
		self.z_pos = 0.0

		# Affects selection area and rejects barrier placement inside area.
		self.half_width = 0.0

		# Affects selection area below object.
		self.pad_bottom = 0.0

		# Affects selection area and rejects barrier placement inside area.
		self.half_depth = 0.0

		# Unknown effect. Possibly vertical offset of box, yet testing was inconclusive.
		self.u_6 = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pad_top', Float, (0, None), (False, None)
		yield 'z_pos', Float, (0, None), (False, None)
		yield 'half_width', Float, (0, None), (False, None)
		yield 'pad_bottom', Float, (0, None), (False, None)
		yield 'half_depth', Float, (0, None), (False, None)
		yield 'u_6', Float, (0, None), (False, None)
