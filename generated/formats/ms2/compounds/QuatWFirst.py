from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class QuatWFirst(BaseStruct):

	__name__ = 'QuatWFirst'

	_import_path = 'generated.formats.ms2.compounds.QuatWFirst'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.w = 1.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'w', Float, (0, None), (False, 1.0)
		yield 'x', Float, (0, None), (False, 0.0)
		yield 'y', Float, (0, None), (False, 0.0)
		yield 'z', Float, (0, None), (False, 0.0)

	def get_info_str(self, indent=0):
		return f'QuatWFirst [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def __repr__(self):
		return f"[ {self.x:6.3f} {self.y:6.3f} {self.z:6.3f} {self.w:6.3f} ]"

