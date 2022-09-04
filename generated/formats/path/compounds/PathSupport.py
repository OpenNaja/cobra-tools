from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PathSupport(MemStruct):

	__name__ = 'PathSupport'

	_import_path = 'generated.formats.path.compounds.PathSupport'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.distance = 10.0
		self._unk_int_1 = 0
		self.support = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.distance = 10.0
		self._unk_int_1 = 0
		self.support = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.support = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.distance = Float.from_stream(stream, instance.context, 0, None)
		instance._unk_int_1 = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.support, int):
			instance.support.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.support)
		Float.to_stream(stream, instance.distance)
		Uint.to_stream(stream, instance._unk_int_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'support', Pointer, (0, ZString), (False, None)
		yield 'distance', Float, (0, None), (False, 10.0)
		yield '_unk_int_1', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'PathSupport [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* support = {self.fmt_member(self.support, indent+1)}'
		s += f'\n	* distance = {self.fmt_member(self.distance, indent+1)}'
		s += f'\n	* _unk_int_1 = {self.fmt_member(self._unk_int_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
