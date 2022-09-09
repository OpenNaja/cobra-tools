from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.path.compounds.Vector2 import Vector2


class Connector(MemStruct):

	__name__ = 'Connector'

	_import_path = 'generated.formats.path.compounds.Connector'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_vector = Vector2(self.context, 0, None)
		self.model_name = Pointer(self.context, 0, ZString)
		self.joint_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'model_name', Pointer, (0, ZString), (False, None)
		yield 'joint_name', Pointer, (0, ZString), (False, None)
		yield 'unk_vector', Vector2, (0, None), (False, None)
