from generated.formats.base.basic import Ushort
from generated.formats.ms2.compounds.AbstractPointer import AbstractPointer


class JointPointer(AbstractPointer):

	__name__ = 'JointPointer'

	_import_key = 'ms2.compounds.JointPointer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into joint_infos
		self.index = 0
		if set_default:
			self.set_defaults()

	_attribute_list = AbstractPointer._attribute_list + [
		('index', Ushort, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'index', Ushort, (0, None), (False, None)
