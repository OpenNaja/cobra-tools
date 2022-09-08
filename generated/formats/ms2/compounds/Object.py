from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort


class Object(BaseStruct):

	__name__ = 'Object'

	_import_path = 'generated.formats.ms2.compounds.Object'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into material name array
		self.material_index = 0

		# index into mesh array
		self.mesh_index = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.material_index = 0
		self.mesh_index = 0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'material_index', Ushort, (0, None), (False, None)
		yield 'mesh_index', Ushort, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Object [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
