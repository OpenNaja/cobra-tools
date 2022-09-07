from generated.formats.motiongraph.compounds.MGTwo import MGTwo
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TransStructStop(MemStruct):

	"""
	24 bytes
	actually same as above, just don't keep reading here
	"""

	__name__ = 'TransStructStop'

	_import_path = 'generated.formats.motiongraph.compounds.TransStructStop'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.other_states = MGTwo(self.context, 0, None)
		self.another_mrfentry_2 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.other_states = MGTwo(self.context, 0, None)
		self.another_mrfentry_2 = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.another_mrfentry_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.other_states = MGTwo.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.another_mrfentry_2, int):
			instance.another_mrfentry_2.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.another_mrfentry_2)
		MGTwo.to_stream(stream, instance.other_states)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'another_mrfentry_2', Pointer, (0, None), (False, None)
		yield 'other_states', MGTwo, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'TransStructStop [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
