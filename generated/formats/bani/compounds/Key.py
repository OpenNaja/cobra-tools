from generated.base_struct import BaseStruct
from generated.formats.bani.compounds.Vector3Short import Vector3Short
from generated.formats.bani.compounds.Vector3Ushort import Vector3Ushort


class Key(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.euler = Vector3Short(self.context, 0, None)
		self.translation = Vector3Ushort(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.euler = Vector3Short(self.context, 0, None)
		self.translation = Vector3Ushort(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.euler = Vector3Short.from_stream(stream, instance.context, 0, None)
		instance.translation = Vector3Ushort.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Vector3Short.to_stream(stream, instance.euler)
		Vector3Ushort.to_stream(stream, instance.translation)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'euler', Vector3Short, (0, None), (False, None)
		yield 'translation', Vector3Ushort, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Key [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* euler = {self.fmt_member(self.euler, indent+1)}'
		s += f'\n	* translation = {self.fmt_member(self.translation, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
