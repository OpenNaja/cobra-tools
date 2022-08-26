from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.posedriverdef.compounds.Data import Data


class Driver(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'Driver'

	_import_path = 'generated.formats.posedriverdef.compounds.Driver'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.unk_1 = 0
		self.unk_2 = 0
		self.joint_name = Pointer(self.context, 0, ZString)
		self.driven_joint_name = Pointer(self.context, 0, ZString)
		self.data = Pointer(self.context, 0, Data)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.unk_1 = 0
		self.unk_2 = 0
		self.joint_name = Pointer(self.context, 0, ZString)
		self.driven_joint_name = Pointer(self.context, 0, ZString)
		self.data = Pointer(self.context, 0, Data)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.joint_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.a = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.b = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.c = Ushort.from_stream(stream, instance.context, 0, None)
		instance.d = Uint.from_stream(stream, instance.context, 0, None)
		instance.driven_joint_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.unk_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data = Pointer.from_stream(stream, instance.context, 0, Data)
		instance.unk_2 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.joint_name, int):
			instance.joint_name.arg = 0
		if not isinstance(instance.driven_joint_name, int):
			instance.driven_joint_name.arg = 0
		if not isinstance(instance.data, int):
			instance.data.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.joint_name)
		Ubyte.to_stream(stream, instance.a)
		Ubyte.to_stream(stream, instance.b)
		Ushort.to_stream(stream, instance.c)
		Uint.to_stream(stream, instance.d)
		Pointer.to_stream(stream, instance.driven_joint_name)
		Uint64.to_stream(stream, instance.unk_1)
		Pointer.to_stream(stream, instance.data)
		Uint64.to_stream(stream, instance.unk_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'joint_name', Pointer, (0, ZString), (False, None)
		yield 'a', Ubyte, (0, None), (False, None)
		yield 'b', Ubyte, (0, None), (False, None)
		yield 'c', Ushort, (0, None), (False, None)
		yield 'd', Uint, (0, None), (False, None)
		yield 'driven_joint_name', Pointer, (0, ZString), (False, None)
		yield 'unk_1', Uint64, (0, None), (False, None)
		yield 'data', Pointer, (0, Data), (False, None)
		yield 'unk_2', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Driver [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* joint_name = {self.fmt_member(self.joint_name, indent+1)}'
		s += f'\n	* a = {self.fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {self.fmt_member(self.b, indent+1)}'
		s += f'\n	* c = {self.fmt_member(self.c, indent+1)}'
		s += f'\n	* d = {self.fmt_member(self.d, indent+1)}'
		s += f'\n	* driven_joint_name = {self.fmt_member(self.driven_joint_name, indent+1)}'
		s += f'\n	* unk_1 = {self.fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* data = {self.fmt_member(self.data, indent+1)}'
		s += f'\n	* unk_2 = {self.fmt_member(self.unk_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
