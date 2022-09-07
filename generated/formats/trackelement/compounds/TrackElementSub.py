from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackElementSub(MemStruct):

	"""
	PC: 32
	"""

	__name__ = 'TrackElementSub'

	_import_path = 'generated.formats.trackelement.compounds.TrackElementSub'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = 0
		self.catwalk_right_lsm = Pointer(self.context, 0, ZString)
		self.catwalk_left_lsm = Pointer(self.context, 0, ZString)
		self.catwalk_both_lsm = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk_0 = 0
		self.catwalk_right_lsm = Pointer(self.context, 0, ZString)
		self.catwalk_left_lsm = Pointer(self.context, 0, ZString)
		self.catwalk_both_lsm = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.catwalk_right_lsm = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.catwalk_left_lsm = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.catwalk_both_lsm = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.unk_0 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.catwalk_right_lsm, int):
			instance.catwalk_right_lsm.arg = 0
		if not isinstance(instance.catwalk_left_lsm, int):
			instance.catwalk_left_lsm.arg = 0
		if not isinstance(instance.catwalk_both_lsm, int):
			instance.catwalk_both_lsm.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.catwalk_right_lsm)
		Pointer.to_stream(stream, instance.catwalk_left_lsm)
		Pointer.to_stream(stream, instance.catwalk_both_lsm)
		Uint64.to_stream(stream, instance.unk_0)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'catwalk_right_lsm', Pointer, (0, ZString), (False, None)
		yield 'catwalk_left_lsm', Pointer, (0, ZString), (False, None)
		yield 'catwalk_both_lsm', Pointer, (0, ZString), (False, None)
		yield 'unk_0', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'TrackElementSub [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
