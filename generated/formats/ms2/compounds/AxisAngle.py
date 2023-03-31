from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class AxisAngle(BaseStruct):

	__name__ = 'AxisAngle'

	_import_key = 'ms2.compounds.AxisAngle'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = 1.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('a', Float, (0, None), (False, 1.0), None)
		yield ('x', Float, (0, None), (False, 0.0), None)
		yield ('y', Float, (0, None), (False, 0.0), None)
		yield ('z', Float, (0, None), (False, 0.0), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', Float, (0, None), (False, 1.0)
		yield 'x', Float, (0, None), (False, 0.0)
		yield 'y', Float, (0, None), (False, 0.0)
		yield 'z', Float, (0, None), (False, 0.0)


AxisAngle.init_attributes()
