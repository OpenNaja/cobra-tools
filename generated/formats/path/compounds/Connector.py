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

	def set_defaults(self):
		super().set_defaults()
		self.unk_vector = Vector2(self.context, 0, None)
		self.model_name = Pointer(self.context, 0, ZString)
		self.joint_name = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.model_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.joint_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.unk_vector = Vector2.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.model_name, int):
			instance.model_name.arg = 0
		if not isinstance(instance.joint_name, int):
			instance.joint_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.model_name)
		Pointer.to_stream(stream, instance.joint_name)
		Vector2.to_stream(stream, instance.unk_vector)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'model_name', Pointer, (0, ZString), (False, None)
		yield 'joint_name', Pointer, (0, ZString), (False, None)
		yield 'unk_vector', Vector2, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Connector [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
