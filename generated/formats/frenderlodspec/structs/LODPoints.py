from generated.array import Array
from generated.formats.frenderlodspec.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class LODPoints(MemStruct):

	__name__ = 'LODPoints'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.discard_at_lod = name_type_map['Ushort'](self.context, 0, None)
		self.max_lods = name_type_map['Ushort'].from_value(6)
		self.lod_points = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.pixel_size_off = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'discard_at_lod', name_type_map['Ushort'], (0, None), (False, None), (lambda context: not (context.version == 18), None)
		yield 'max_lods', name_type_map['Ushort'], (0, None), (False, 6), (lambda context: not (context.version == 18), None)
		yield 'lod_points', Array, (0, None, (5,), name_type_map['Float']), (False, None), (None, None)
		yield 'pixel_size_off', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if not (instance.context.version == 18):
			yield 'discard_at_lod', name_type_map['Ushort'], (0, None), (False, None)
			yield 'max_lods', name_type_map['Ushort'], (0, None), (False, 6)
		yield 'lod_points', Array, (0, None, (5,), name_type_map['Float']), (False, None)
		yield 'pixel_size_off', name_type_map['Float'], (0, None), (False, None)
