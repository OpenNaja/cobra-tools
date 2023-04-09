from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LodSpecItem(MemStruct):

	__name__ = 'LodSpecItem'

	_import_key = 'frenderlodspec.compounds.LodSpecItem'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unknown_1 = 0
		self.max_model_bounding_sphere_radius = 0.0
		self.flags_1 = 0
		self.flags_2 = 0
		self.lod_point_0 = 0.0
		self.lod_point_1 = 0.0
		self.lod_point_2 = 0.0
		self.lod_point_3 = 0.0
		self.lod_point_4 = 0.0
		self.pixel_size_off = 0.0
		self.unknown_2 = 0
		self.unknown_3 = 0
		self.unknown_4 = 0
		self.group_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('group_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('unknown_1', Uint, (0, None), (False, None), (None, None))
		yield ('max_model_bounding_sphere_radius', Float, (0, None), (False, None), (None, None))
		yield ('flags_1', Ushort, (0, None), (False, None), (None, None))
		yield ('flags_2', Ushort, (0, None), (False, None), (None, None))
		yield ('lod_point_0', Float, (0, None), (False, None), (None, None))
		yield ('lod_point_1', Float, (0, None), (False, None), (None, None))
		yield ('lod_point_2', Float, (0, None), (False, None), (None, None))
		yield ('lod_point_3', Float, (0, None), (False, None), (None, None))
		yield ('lod_point_4', Float, (0, None), (False, None), (None, None))
		yield ('pixel_size_off', Float, (0, None), (False, None), (None, None))
		yield ('unknown_2', Uint, (0, None), (False, None), (None, None))
		yield ('unknown_3', Uint, (0, None), (False, None), (None, None))
		yield ('unknown_4', Uint, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'group_name', Pointer, (0, ZString), (False, None)
		yield 'unknown_1', Uint, (0, None), (False, None)
		yield 'max_model_bounding_sphere_radius', Float, (0, None), (False, None)
		yield 'flags_1', Ushort, (0, None), (False, None)
		yield 'flags_2', Ushort, (0, None), (False, None)
		yield 'lod_point_0', Float, (0, None), (False, None)
		yield 'lod_point_1', Float, (0, None), (False, None)
		yield 'lod_point_2', Float, (0, None), (False, None)
		yield 'lod_point_3', Float, (0, None), (False, None)
		yield 'lod_point_4', Float, (0, None), (False, None)
		yield 'pixel_size_off', Float, (0, None), (False, None)
		yield 'unknown_2', Uint, (0, None), (False, None)
		yield 'unknown_3', Uint, (0, None), (False, None)
		yield 'unknown_4', Uint, (0, None), (False, None)
