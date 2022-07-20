from source.formats.base.basic import fmt_member
import generated.formats.path.compound.Connector
import generated.formats.path.compound.ConnectorMultiJoint
import generated.formats.path.compound.Footer
import generated.formats.path.compound.Pillar
import generated.formats.path.compound.SupportSetData
import numpy
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer
from generated.formats.path.compound.Vector2 import Vector2
from generated.formats.path.compound.Vector3 import Vector3


class SupportSetRoot(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.padding = 0
		self.unk_vector_1 = 0
		self.unk_vector_2 = 0
		self.unk_vector_3 = 0
		self.unk_int_1 = 0
		self.num_connector_1 = 0
		self.num_connector_2 = 0
		self.unk_ints = 0
		self.padding_2 = 0
		self.num_data = 0
		self.connector_1 = 0
		self.connector_2 = 0
		self.pillar = 0
		self.footer = 0
		self.data = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.padding = 0
		self.unk_vector_1 = Vector3(self.context, 0, None)
		self.unk_vector_2 = Vector2(self.context, 0, None)
		self.unk_vector_3 = Vector3(self.context, 0, None)
		self.unk_int_1 = 0
		self.num_connector_1 = 0
		self.num_connector_2 = 0
		self.unk_ints = numpy.zeros((7,), dtype=numpy.dtype('uint32'))
		self.padding_2 = 0
		self.num_data = 0
		self.connector_1 = ArrayPointer(self.context, self.num_connector_1, generated.formats.path.compound.Connector.Connector)
		self.connector_2 = ArrayPointer(self.context, self.num_connector_2, generated.formats.path.compound.ConnectorMultiJoint.ConnectorMultiJoint)
		self.pillar = Pointer(self.context, 0, generated.formats.path.compound.Pillar.Pillar)
		self.footer = Pointer(self.context, 0, generated.formats.path.compound.Footer.Footer)
		self.data = ArrayPointer(self.context, self.num_data, generated.formats.path.compound.SupportSetData.SupportSetData)

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
		instance.connector_1 = ArrayPointer.from_stream(stream, instance.context, instance.num_connector_1, generated.formats.path.compound.Connector.Connector)
		instance.connector_2 = ArrayPointer.from_stream(stream, instance.context, instance.num_connector_2, generated.formats.path.compound.ConnectorMultiJoint.ConnectorMultiJoint)
		instance.pillar = Pointer.from_stream(stream, instance.context, 0, generated.formats.path.compound.Pillar.Pillar)
		instance.footer = Pointer.from_stream(stream, instance.context, 0, generated.formats.path.compound.Footer.Footer)
		instance.padding = stream.read_uint64()
		instance.unk_vector_1 = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_vector_2 = Vector2.from_stream(stream, instance.context, 0, None)
		instance.unk_vector_3 = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_int_1 = stream.read_uint()
		instance.num_connector_1 = stream.read_uint()
		instance.num_connector_2 = stream.read_uint()
		instance.unk_ints = stream.read_uints((7,))
		instance.padding_2 = stream.read_uint64()
		instance.data = ArrayPointer.from_stream(stream, instance.context, instance.num_data, generated.formats.path.compound.SupportSetData.SupportSetData)
		instance.num_data = stream.read_uint()
		instance.connector_1.arg = instance.num_connector_1
		instance.connector_2.arg = instance.num_connector_2
		instance.pillar.arg = 0
		instance.footer.arg = 0
		instance.data.arg = instance.num_data

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.connector_1)
		ArrayPointer.to_stream(stream, instance.connector_2)
		Pointer.to_stream(stream, instance.pillar)
		Pointer.to_stream(stream, instance.footer)
		stream.write_uint64(instance.padding)
		Vector3.to_stream(stream, instance.unk_vector_1)
		Vector2.to_stream(stream, instance.unk_vector_2)
		Vector3.to_stream(stream, instance.unk_vector_3)
		stream.write_uint(instance.unk_int_1)
		stream.write_uint(instance.num_connector_1)
		stream.write_uint(instance.num_connector_2)
		stream.write_uints(instance.unk_ints)
		stream.write_uint64(instance.padding_2)
		ArrayPointer.to_stream(stream, instance.data)
		stream.write_uint(instance.num_data)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'SupportSetRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* connector_1 = {fmt_member(self.connector_1, indent+1)}'
		s += f'\n	* connector_2 = {fmt_member(self.connector_2, indent+1)}'
		s += f'\n	* pillar = {fmt_member(self.pillar, indent+1)}'
		s += f'\n	* footer = {fmt_member(self.footer, indent+1)}'
		s += f'\n	* padding = {fmt_member(self.padding, indent+1)}'
		s += f'\n	* unk_vector_1 = {fmt_member(self.unk_vector_1, indent+1)}'
		s += f'\n	* unk_vector_2 = {fmt_member(self.unk_vector_2, indent+1)}'
		s += f'\n	* unk_vector_3 = {fmt_member(self.unk_vector_3, indent+1)}'
		s += f'\n	* unk_int_1 = {fmt_member(self.unk_int_1, indent+1)}'
		s += f'\n	* num_connector_1 = {fmt_member(self.num_connector_1, indent+1)}'
		s += f'\n	* num_connector_2 = {fmt_member(self.num_connector_2, indent+1)}'
		s += f'\n	* unk_ints = {fmt_member(self.unk_ints, indent+1)}'
		s += f'\n	* padding_2 = {fmt_member(self.padding_2, indent+1)}'
		s += f'\n	* data = {fmt_member(self.data, indent+1)}'
		s += f'\n	* num_data = {fmt_member(self.num_data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
