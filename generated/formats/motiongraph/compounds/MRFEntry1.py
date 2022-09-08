from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MRFEntry1(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'MRFEntry1'

	_import_path = 'generated.formats.motiongraph.compounds.MRFEntry1'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = Pointer(self.context, 0, MRFEntry1._import_path_map["generated.formats.motiongraph.compounds.MRFMember1"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.value = Pointer(self.context, 0, MRFEntry1._import_path_map["generated.formats.motiongraph.compounds.MRFMember1"])

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'value', Pointer, (0, MRFEntry1._import_path_map["generated.formats.motiongraph.compounds.MRFMember1"]), (False, None)

	def get_info_str(self, indent=0):
		return f'MRFEntry1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
