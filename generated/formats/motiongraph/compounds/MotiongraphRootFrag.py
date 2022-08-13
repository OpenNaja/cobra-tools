import generated.formats.motiongraph.compounds.Activities
import generated.formats.motiongraph.compounds.MRFArray1
import generated.formats.motiongraph.compounds.MRFArray2
import generated.formats.motiongraph.compounds.XMLArray
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MotiongraphRootFrag(MemStruct):

	"""
	64 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_activities = 0
		self.count_1 = 0
		self.count_2 = 0
		self.num_xmls = 0
		self.activities = Pointer(self.context, self.num_activities, generated.formats.motiongraph.compounds.Activities.Activities)
		self.ptr_1 = Pointer(self.context, self.count_1, generated.formats.motiongraph.compounds.MRFArray1.MRFArray1)
		self.ptr_2 = Pointer(self.context, self.count_2, generated.formats.motiongraph.compounds.MRFArray2.MRFArray2)
		self.ptr_xmls = Pointer(self.context, self.num_xmls, generated.formats.motiongraph.compounds.XMLArray.XMLArray)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.num_activities = 0
		self.count_1 = 0
		self.count_2 = 0
		self.num_xmls = 0
		self.activities = Pointer(self.context, self.num_activities, generated.formats.motiongraph.compounds.Activities.Activities)
		self.ptr_1 = Pointer(self.context, self.count_1, generated.formats.motiongraph.compounds.MRFArray1.MRFArray1)
		self.ptr_2 = Pointer(self.context, self.count_2, generated.formats.motiongraph.compounds.MRFArray2.MRFArray2)
		self.ptr_xmls = Pointer(self.context, self.num_xmls, generated.formats.motiongraph.compounds.XMLArray.XMLArray)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.num_activities = stream.read_uint64()
		instance.activities = Pointer.from_stream(stream, instance.context, instance.num_activities, generated.formats.motiongraph.compounds.Activities.Activities)
		instance.count_1 = stream.read_uint64()
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, instance.count_1, generated.formats.motiongraph.compounds.MRFArray1.MRFArray1)
		instance.count_2 = stream.read_uint64()
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, instance.count_2, generated.formats.motiongraph.compounds.MRFArray2.MRFArray2)
		instance.num_xmls = stream.read_uint64()
		instance.ptr_xmls = Pointer.from_stream(stream, instance.context, instance.num_xmls, generated.formats.motiongraph.compounds.XMLArray.XMLArray)
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
		stream.write_uint64(instance.num_activities)
		Pointer.to_stream(stream, instance.activities)
		stream.write_uint64(instance.count_1)
		Pointer.to_stream(stream, instance.ptr_1)
		stream.write_uint64(instance.count_2)
		Pointer.to_stream(stream, instance.ptr_2)
		stream.write_uint64(instance.num_xmls)
		Pointer.to_stream(stream, instance.ptr_xmls)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield 'num_activities', Uint64, (0, None)
		yield 'activities', Pointer, (instance.num_activities, generated.formats.motiongraph.compounds.Activities.Activities)
		yield 'count_1', Uint64, (0, None)
		yield 'ptr_1', Pointer, (instance.count_1, generated.formats.motiongraph.compounds.MRFArray1.MRFArray1)
		yield 'count_2', Uint64, (0, None)
		yield 'ptr_2', Pointer, (instance.count_2, generated.formats.motiongraph.compounds.MRFArray2.MRFArray2)
		yield 'num_xmls', Uint64, (0, None)
		yield 'ptr_xmls', Pointer, (instance.num_xmls, generated.formats.motiongraph.compounds.XMLArray.XMLArray)

	def get_info_str(self, indent=0):
		return f'MotiongraphRootFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* num_activities = {self.fmt_member(self.num_activities, indent+1)}'
		s += f'\n	* activities = {self.fmt_member(self.activities, indent+1)}'
		s += f'\n	* count_1 = {self.fmt_member(self.count_1, indent+1)}'
		s += f'\n	* ptr_1 = {self.fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* count_2 = {self.fmt_member(self.count_2, indent+1)}'
		s += f'\n	* ptr_2 = {self.fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* num_xmls = {self.fmt_member(self.num_xmls, indent+1)}'
		s += f'\n	* ptr_xmls = {self.fmt_member(self.ptr_xmls, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
