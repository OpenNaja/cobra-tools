from generated.base_struct import BaseStruct
from generated.formats.bani.compounds.Vector3Short import Vector3Short
from generated.formats.bani.compounds.Vector3Ushort import Vector3Ushort


class Key(BaseStruct):

	__name__ = 'Key'

	_import_key = 'bani.compounds.Key'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.euler = Vector3Short(self.context, 0, None)
		self.translation = Vector3Ushort(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('euler', Vector3Short, (0, None), (False, None), (None, None))
		yield ('translation', Vector3Ushort, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'euler', Vector3Short, (0, None), (False, None)
		yield 'translation', Vector3Ushort, (0, None), (False, None)
