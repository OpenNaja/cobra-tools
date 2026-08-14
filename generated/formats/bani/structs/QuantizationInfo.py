from generated.base_struct import BaseStruct
from generated.formats.bani.imports import name_type_map


class QuantizationInfo(BaseStruct):

	"""
	8 bytes
	"""

	__name__ = 'QuantizationInfo'

	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Multiplier for translation de-quantization
		self.scale = name_type_map['Float'](self.context, 0, None)

		# Bias (minimum bound) for translation de-quantization
		self.bias = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'scale', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'bias', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'scale', name_type_map['Float'], (0, None), (False, None)
		yield 'bias', name_type_map['Float'], (0, None), (False, None)
