import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackedRideCarRoot(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'TrackedRideCarRoot'

	_import_key = 'trackedridecar.compounds.TrackedRideCarRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.sub_count = 0
		self.total_vecs_count = 0
		self.vec = Array(self.context, 0, None, (0,), Float)
		self.zero_0 = 0
		self.zero_1 = 0
		self.sub = ArrayPointer(self.context, self.sub_count, TrackedRideCarRoot._import_map["trackedridecar.compounds.TrackedRideCarSub"])
		self.some_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('sub', ArrayPointer, (None, TrackedRideCarRoot._import_map["trackedridecar.compounds.TrackedRideCarSub"]), (False, None), None)
		yield ('sub_count', Uint, (0, None), (False, None), None)
		yield ('total_vecs_count', Uint, (0, None), (False, None), None)
		yield ('vec', Array, (0, None, (3,), Float), (False, None), None)
		yield ('zero_0', Uint, (0, None), (False, None), None)
		yield ('some_name', Pointer, (0, ZString), (False, None), None)
		yield ('zero_1', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'sub', ArrayPointer, (instance.sub_count, TrackedRideCarRoot._import_map["trackedridecar.compounds.TrackedRideCarSub"]), (False, None)
		yield 'sub_count', Uint, (0, None), (False, None)
		yield 'total_vecs_count', Uint, (0, None), (False, None)
		yield 'vec', Array, (0, None, (3,), Float), (False, None)
		yield 'zero_0', Uint, (0, None), (False, None)
		yield 'some_name', Pointer, (0, ZString), (False, None)
		yield 'zero_1', Uint64, (0, None), (False, None)


TrackedRideCarRoot.init_attributes()
