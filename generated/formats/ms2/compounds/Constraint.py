from generated.base_struct import BaseStruct
from generated.formats.ms2.compounds.JointPointer import JointPointer


class Constraint(BaseStruct):

	__name__ = 'Constraint'

	_import_key = 'ms2.compounds.Constraint'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.parent = JointPointer(self.context, 0, None)
		self.child = JointPointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('parent', JointPointer, (0, None), (False, None), (None, None))
		yield ('child', JointPointer, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'parent', JointPointer, (0, None), (False, None)
		yield 'child', JointPointer, (0, None), (False, None)
