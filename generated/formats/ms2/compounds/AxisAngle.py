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

	_attribute_list = BaseStruct._attribute_list + [
		('a', Float, (0, None), (False, 1.0), None),
		('x', Float, (0, None), (False, 0.0), None),
		('y', Float, (0, None), (False, 0.0), None),
		('z', Float, (0, None), (False, 0.0), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', Float, (0, None), (False, 1.0)
		yield 'x', Float, (0, None), (False, 0.0)
		yield 'y', Float, (0, None), (False, 0.0)
		yield 'z', Float, (0, None), (False, 0.0)
