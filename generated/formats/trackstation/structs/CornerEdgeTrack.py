from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class CornerEdgeTrack(MemStruct):

	"""
	PC:  320 bytes
	PC2: 320 bytes
	unused on PZ
	"""

	__name__ = 'CornerEdgeTrack'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.corner = name_type_map['CommonChunk'](self.context, 0, None)
		self.edge = name_type_map['CommonChunk'](self.context, 0, None)
		self.track = name_type_map['CommonChunk'](self.context, 0, None)
		self.zero = name_type_map['Uint64'].from_value(0)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'corner', name_type_map['CommonChunk'], (0, None), (False, None), (None, None)
		yield 'edge', name_type_map['CommonChunk'], (0, None), (False, None), (None, None)
		yield 'track', name_type_map['CommonChunk'], (0, None), (False, None), (None, None)
		yield 'zero', name_type_map['Uint64'], (0, None), (True, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'corner', name_type_map['CommonChunk'], (0, None), (False, None)
		yield 'edge', name_type_map['CommonChunk'], (0, None), (False, None)
		yield 'track', name_type_map['CommonChunk'], (0, None), (False, None)
		yield 'zero', name_type_map['Uint64'], (0, None), (True, 0)
