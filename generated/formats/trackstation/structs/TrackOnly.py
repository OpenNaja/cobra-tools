from generated.formats.trackstation.imports import name_type_map
from generated.formats.trackstation.structs.CommonChunk import CommonChunk


class TrackOnly(CommonChunk):

	"""
	PZ and PC: 112 bytes
	"""

	__name__ = 'TrackOnly'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_2 = name_type_map['Uint64'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None)
