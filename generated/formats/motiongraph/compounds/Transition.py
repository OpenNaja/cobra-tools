from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Transition(MemStruct):

	"""
	40 bytes
	only used if transition is in 'id'
	"""

	__name__ = 'Transition'

	_import_path = 'generated.formats.motiongraph.compounds.Transition'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.ptr_0 = Pointer(self.context, self.count_1, Transition._import_path_map["generated.formats.motiongraph.compounds.PtrList"])
		self.ptr_1 = Pointer(self.context, self.count_2, Transition._import_path_map["generated.formats.motiongraph.compounds.TransStructArray"])
		self.id = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.ptr_0 = Pointer(self.context, self.count_1, Transition._import_path_map["generated.formats.motiongraph.compounds.PtrList"])
		self.ptr_1 = Pointer(self.context, self.count_2, Transition._import_path_map["generated.formats.motiongraph.compounds.TransStructArray"])
		self.id = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.count_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.count_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, instance.count_1, Transition._import_path_map["generated.formats.motiongraph.compounds.PtrList"])
		instance.count_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, instance.count_2, Transition._import_path_map["generated.formats.motiongraph.compounds.TransStructArray"])
		instance.id = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.ptr_0, int):
			instance.ptr_0.arg = instance.count_1
		if not isinstance(instance.ptr_1, int):
			instance.ptr_1.arg = instance.count_2
		if not isinstance(instance.id, int):
			instance.id.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.count_0)
		Uint.to_stream(stream, instance.count_1)
		Pointer.to_stream(stream, instance.ptr_0)
		Uint64.to_stream(stream, instance.count_2)
		Pointer.to_stream(stream, instance.ptr_1)
		Pointer.to_stream(stream, instance.id)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'count_0', Uint, (0, None), (False, None)
		yield 'count_1', Uint, (0, None), (False, None)
		yield 'ptr_0', Pointer, (instance.count_1, Transition._import_path_map["generated.formats.motiongraph.compounds.PtrList"]), (False, None)
		yield 'count_2', Uint64, (0, None), (False, None)
		yield 'ptr_1', Pointer, (instance.count_2, Transition._import_path_map["generated.formats.motiongraph.compounds.TransStructArray"]), (False, None)
		yield 'id', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'Transition [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
