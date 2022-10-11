from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PhysicsSurfaceXMLResRoot(MemStruct):

	"""
	# There is an initial 'default' surface, these params are the same as in SurfacePhysicsInfo
	"""

	__name__ = 'PhysicsSurfaceXMLResRoot'

	_import_key = 'physicssurfacesxmlres.compounds.PhysicsSurfaceXMLResRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float_1 = 0.0
		self.float_2 = 0.0
		self.float_3 = 0.0
		self.float_4 = 0.0
		self.unk_64_1 = 0
		self.count = 0
		self.short_2 = 0
		self.unk_32_1 = 0
		self.unk_64_4 = 0
		self.unk_64_5 = 0
		self.unk_64_6 = 0
		self.unk_64_7 = 0
		self.unk_64_8 = 0
		self.unk_64_9 = 0
		self.unk_64_10 = 0
		self.default_surface_name = Pointer(self.context, 0, ZString)
		self.name_1 = Pointer(self.context, 0, ZString)
		self.name_2 = Pointer(self.context, 0, ZString)
		self.ptr_1 = Pointer(self.context, 0, PhysicsSurfaceXMLResRoot._import_map["physicssurfacesxmlres.compounds.EmptyStruct"])
		self.ptr_2 = ArrayPointer(self.context, self.count, PhysicsSurfaceXMLResRoot._import_map["physicssurfacesxmlres.compounds.SurfacePhysicsInfo"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('default_surface_name', Pointer, (0, ZString), (False, None), None),
		('float_1', Float, (0, None), (False, None), None),
		('float_2', Float, (0, None), (False, None), None),
		('float_3', Float, (0, None), (False, None), None),
		('float_4', Float, (0, None), (False, None), None),
		('unk_64_1', Uint64, (0, None), (False, None), None),
		('name_1', Pointer, (0, ZString), (False, None), None),
		('name_2', Pointer, (0, ZString), (False, None), None),
		('ptr_1', Pointer, (0, None), (False, None), None),
		('ptr_2', ArrayPointer, (None, None), (False, None), None),
		('count', Ushort, (0, None), (False, None), None),
		('short_2', Ushort, (0, None), (False, None), None),
		('unk_32_1', Uint, (0, None), (False, None), None),
		('unk_64_4', Uint64, (0, None), (False, None), None),
		('unk_64_5', Uint64, (0, None), (False, None), None),
		('unk_64_6', Uint64, (0, None), (False, None), None),
		('unk_64_7', Uint64, (0, None), (False, None), None),
		('unk_64_8', Uint64, (0, None), (False, None), None),
		('unk_64_9', Uint64, (0, None), (False, None), None),
		('unk_64_10', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'default_surface_name', Pointer, (0, ZString), (False, None)
		yield 'float_1', Float, (0, None), (False, None)
		yield 'float_2', Float, (0, None), (False, None)
		yield 'float_3', Float, (0, None), (False, None)
		yield 'float_4', Float, (0, None), (False, None)
		yield 'unk_64_1', Uint64, (0, None), (False, None)
		yield 'name_1', Pointer, (0, ZString), (False, None)
		yield 'name_2', Pointer, (0, ZString), (False, None)
		yield 'ptr_1', Pointer, (0, PhysicsSurfaceXMLResRoot._import_map["physicssurfacesxmlres.compounds.EmptyStruct"]), (False, None)
		yield 'ptr_2', ArrayPointer, (instance.count, PhysicsSurfaceXMLResRoot._import_map["physicssurfacesxmlres.compounds.SurfacePhysicsInfo"]), (False, None)
		yield 'count', Ushort, (0, None), (False, None)
		yield 'short_2', Ushort, (0, None), (False, None)
		yield 'unk_32_1', Uint, (0, None), (False, None)
		yield 'unk_64_4', Uint64, (0, None), (False, None)
		yield 'unk_64_5', Uint64, (0, None), (False, None)
		yield 'unk_64_6', Uint64, (0, None), (False, None)
		yield 'unk_64_7', Uint64, (0, None), (False, None)
		yield 'unk_64_8', Uint64, (0, None), (False, None)
		yield 'unk_64_9', Uint64, (0, None), (False, None)
		yield 'unk_64_10', Uint64, (0, None), (False, None)
