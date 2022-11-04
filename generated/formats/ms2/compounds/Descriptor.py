from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort


class Descriptor(BaseStruct):

	__name__ = 'Descriptor'

	_import_key = 'ms2.compounds.Descriptor'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into joint_infos
		self.parent = 0

		# index into joint_infos
		self.child = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('parent', Ushort, (0, None), (False, None), None),
		('child', Ushort, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'parent', Ushort, (0, None), (False, None)
		yield 'child', Ushort, (0, None), (False, None)
