from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.bnk.compounds.DataPointer import DataPointer


class DIDXSection(BaseStruct):

	"""
	second Section of a soundback aux
	"""

	__name__ = 'DIDXSection'

	_import_path = 'generated.formats.bnk.compounds.DIDXSection'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of following data
		self.length = 0
		self.data_pointers = Array(self.context, 0, None, (0,), DataPointer)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.length = 0
		self.data_pointers = Array(self.context, 0, None, (int(self.length / 12),), DataPointer)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.length = Uint.from_stream(stream, instance.context, 0, None)
		instance.data_pointers = Array.from_stream(stream, instance.context, 0, None, (int(instance.length / 12),), DataPointer)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.length)
		Array.to_stream(stream, instance.data_pointers, instance.context, 0, None, (int(instance.length / 12),), DataPointer)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'length', Uint, (0, None), (False, None)
		yield 'data_pointers', Array, (0, None, (int(instance.length / 12),), DataPointer), (False, None)

	def get_info_str(self, indent=0):
		return f'DIDXSection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
