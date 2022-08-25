import generated.formats.base.basic
import generated.formats.path.compounds.Joint
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ConnectorMultiJoint(MemStruct):

	__name__ = 'ConnectorMultiJoint'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.padding = 0
		self.num_joints = 0
		self.unk_float_1 = 0.0
		self.unk_int_1 = 0
		self.padding_2 = 0
		self.model_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.joints = ArrayPointer(self.context, self.num_joints, generated.formats.path.compounds.Joint.Joint)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.padding = 0
		self.num_joints = 0
		self.unk_float_1 = 0.0
		self.unk_int_1 = 0
		self.padding_2 = 0
		self.model_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.joints = ArrayPointer(self.context, self.num_joints, generated.formats.path.compounds.Joint.Joint)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.model_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.padding = Uint64.from_stream(stream, instance.context, 0, None)
		instance.joints = ArrayPointer.from_stream(stream, instance.context, instance.num_joints, generated.formats.path.compounds.Joint.Joint)
		instance.num_joints = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_float_1 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_int_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.padding_2 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.model_name, int):
			instance.model_name.arg = 0
		if not isinstance(instance.joints, int):
			instance.joints.arg = instance.num_joints

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.model_name)
		Uint64.to_stream(stream, instance.padding)
		ArrayPointer.to_stream(stream, instance.joints)
		Uint64.to_stream(stream, instance.num_joints)
		Float.to_stream(stream, instance.unk_float_1)
		Uint.to_stream(stream, instance.unk_int_1)
		Uint64.to_stream(stream, instance.padding_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'model_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'padding', Uint64, (0, None), (True, 0)
		yield 'joints', ArrayPointer, (instance.num_joints, generated.formats.path.compounds.Joint.Joint), (False, None)
		yield 'num_joints', Uint64, (0, None), (False, None)
		yield 'unk_float_1', Float, (0, None), (False, None)
		yield 'unk_int_1', Uint, (0, None), (False, None)
		yield 'padding_2', Uint64, (0, None), (True, 0)

	def get_info_str(self, indent=0):
		return f'ConnectorMultiJoint [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* model_name = {self.fmt_member(self.model_name, indent+1)}'
		s += f'\n	* padding = {self.fmt_member(self.padding, indent+1)}'
		s += f'\n	* joints = {self.fmt_member(self.joints, indent+1)}'
		s += f'\n	* num_joints = {self.fmt_member(self.num_joints, indent+1)}'
		s += f'\n	* unk_float_1 = {self.fmt_member(self.unk_float_1, indent+1)}'
		s += f'\n	* unk_int_1 = {self.fmt_member(self.unk_int_1, indent+1)}'
		s += f'\n	* padding_2 = {self.fmt_member(self.padding_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
