from generated.base_struct import BaseStruct
from generated.formats.base.basic import Normshort


class Vector4H(BaseStruct):

	__name__ = 'Vector4H'

	_import_key = 'manis.compounds.Vector4H'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.w = 0
		self.x = 0
		self.y = 0
		self.z = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('w', Normshort, (0, None), (False, None), None)
		yield ('x', Normshort, (0, None), (False, None), None)
		yield ('y', Normshort, (0, None), (False, None), None)
		yield ('z', Normshort, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'w', Normshort, (0, None), (False, None)
		yield 'x', Normshort, (0, None), (False, None)
		yield 'y', Normshort, (0, None), (False, None)
		yield 'z', Normshort, (0, None), (False, None)


Vector4H.init_attributes()
