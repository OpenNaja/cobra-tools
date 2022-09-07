from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort


class Descriptor(BaseStruct):

	__name__ = 'Descriptor'

	_import_path = 'generated.formats.ms2.compounds.Descriptor'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into joint_infos
		self.parent = 0

		# index into joint_infos
		self.child = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.parent = 0
		self.child = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.parent = Ushort.from_stream(stream, instance.context, 0, None)
		instance.child = Ushort.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Ushort.to_stream(stream, instance.parent)
		Ushort.to_stream(stream, instance.child)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'parent', Ushort, (0, None), (False, None)
		yield 'child', Ushort, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Descriptor [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
