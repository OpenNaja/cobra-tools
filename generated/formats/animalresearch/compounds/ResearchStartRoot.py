from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ResearchStartRoot(MemStruct):

	__name__ = 'ResearchStartRoot'

	_import_path = 'generated.formats.animalresearch.compounds.ResearchStartRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.states = ArrayPointer(self.context, self.count, ResearchStartRoot._import_path_map["generated.formats.animalresearch.compounds.UnlockState"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.states = ArrayPointer(self.context, self.count, ResearchStartRoot._import_path_map["generated.formats.animalresearch.compounds.UnlockState"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.states = ArrayPointer.from_stream(stream, instance.context, instance.count, ResearchStartRoot._import_path_map["generated.formats.animalresearch.compounds.UnlockState"])
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.states, int):
			instance.states.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.states)
		Uint64.to_stream(stream, instance.count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'states', ArrayPointer, (instance.count, ResearchStartRoot._import_path_map["generated.formats.animalresearch.compounds.UnlockState"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ResearchStartRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
