from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbPostSize(MemStruct):

	__name__ = 'HB_PostSize'

	_import_key = 'habitatboundary.structs.HbPostSize'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Post size front and back. Affects navcut and selection.
		self.front_back = 0.0

		# Post size left and right. Affects navcut and selection.
		self.left_right = 0.0

		# Post size above wall. Affects navcut and selection.
		self.top = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'front_back', Float, (0, None), (False, None)
		yield 'left_right', Float, (0, None), (False, None)
		yield 'top', Float, (0, None), (False, None)
