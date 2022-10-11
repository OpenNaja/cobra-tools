from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SurfacePhysicsInfo(MemStruct):

	"""
	# todo: define the right property name for these values
	"""

	__name__ = 'SurfacePhysicsInfo'

	_import_key = 'physicssurfacesxmlres.compounds.SurfacePhysicsInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float_1 = 0.0
		self.float_2 = 0.0
		self.float_3 = 0.0
		self.float_4 = 0.0
		self.unk_64_1 = 0
		self.surface_name = Pointer(self.context, 0, ZString)
		self.name_1 = Pointer(self.context, 0, ZString)
		self.name_2 = Pointer(self.context, 0, ZString)
		self.ptr_1 = Pointer(self.context, 0, SurfacePhysicsInfo._import_map["physicssurfacesxmlres.compounds.EmptyStruct"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('surface_name', Pointer, (0, ZString), (False, None), None),
		('float_1', Float, (0, None), (False, None), None),
		('float_2', Float, (0, None), (False, None), None),
		('float_3', Float, (0, None), (False, None), None),
		('float_4', Float, (0, None), (False, None), None),
		('unk_64_1', Uint64, (0, None), (False, None), None),
		('name_1', Pointer, (0, ZString), (False, None), None),
		('name_2', Pointer, (0, ZString), (False, None), None),
		('ptr_1', Pointer, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'surface_name', Pointer, (0, ZString), (False, None)
		yield 'float_1', Float, (0, None), (False, None)
		yield 'float_2', Float, (0, None), (False, None)
		yield 'float_3', Float, (0, None), (False, None)
		yield 'float_4', Float, (0, None), (False, None)
		yield 'unk_64_1', Uint64, (0, None), (False, None)
		yield 'name_1', Pointer, (0, ZString), (False, None)
		yield 'name_2', Pointer, (0, ZString), (False, None)
		yield 'ptr_1', Pointer, (0, SurfacePhysicsInfo._import_map["physicssurfacesxmlres.compounds.EmptyStruct"]), (False, None)
