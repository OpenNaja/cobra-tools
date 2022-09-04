from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MotiongraphRootFrag(MemStruct):

	"""
	64 bytes
	"""

	__name__ = 'MotiongraphRootFrag'

	_import_path = 'generated.formats.motiongraph.compounds.MotiongraphRootFrag'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_activities = 0
		self.count_1 = 0
		self.count_2 = 0
		self.num_xmls = 0
		self.activities = Pointer(self.context, self.num_activities, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.Activities"])
		self.ptr_1 = Pointer(self.context, self.count_1, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.MRFArray1"])
		self.ptr_2 = Pointer(self.context, self.count_2, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.MRFArray2"])
		self.ptr_xmls = Pointer(self.context, self.num_xmls, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.XMLArray"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.num_activities = 0
		self.count_1 = 0
		self.count_2 = 0
		self.num_xmls = 0
		self.activities = Pointer(self.context, self.num_activities, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.Activities"])
		self.ptr_1 = Pointer(self.context, self.count_1, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.MRFArray1"])
		self.ptr_2 = Pointer(self.context, self.count_2, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.MRFArray2"])
		self.ptr_xmls = Pointer(self.context, self.num_xmls, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.XMLArray"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.num_activities = Uint64.from_stream(stream, instance.context, 0, None)
		instance.activities = Pointer.from_stream(stream, instance.context, instance.num_activities, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.Activities"])
		instance.count_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, instance.count_1, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.MRFArray1"])
		instance.count_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, instance.count_2, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.MRFArray2"])
		instance.num_xmls = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr_xmls = Pointer.from_stream(stream, instance.context, instance.num_xmls, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.XMLArray"])
		if not isinstance(instance.activities, int):
			instance.activities.arg = instance.num_activities
		if not isinstance(instance.ptr_1, int):
			instance.ptr_1.arg = instance.count_1
		if not isinstance(instance.ptr_2, int):
			instance.ptr_2.arg = instance.count_2
		if not isinstance(instance.ptr_xmls, int):
			instance.ptr_xmls.arg = instance.num_xmls

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.num_activities)
		Pointer.to_stream(stream, instance.activities)
		Uint64.to_stream(stream, instance.count_1)
		Pointer.to_stream(stream, instance.ptr_1)
		Uint64.to_stream(stream, instance.count_2)
		Pointer.to_stream(stream, instance.ptr_2)
		Uint64.to_stream(stream, instance.num_xmls)
		Pointer.to_stream(stream, instance.ptr_xmls)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'num_activities', Uint64, (0, None), (False, None)
		yield 'activities', Pointer, (instance.num_activities, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.Activities"]), (False, None)
		yield 'count_1', Uint64, (0, None), (False, None)
		yield 'ptr_1', Pointer, (instance.count_1, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.MRFArray1"]), (False, None)
		yield 'count_2', Uint64, (0, None), (False, None)
		yield 'ptr_2', Pointer, (instance.count_2, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.MRFArray2"]), (False, None)
		yield 'num_xmls', Uint64, (0, None), (False, None)
		yield 'ptr_xmls', Pointer, (instance.num_xmls, MotiongraphRootFrag._import_path_map["generated.formats.motiongraph.compounds.XMLArray"]), (False, None)

	def get_info_str(self, indent=0):
		return f'MotiongraphRootFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
