import generated.formats.path.compounds.Connector
import generated.formats.path.compounds.ConnectorMultiJoint
import generated.formats.path.compounds.Footer
import generated.formats.path.compounds.Pillar
import generated.formats.path.compounds.SupportSetData
import numpy
from generated.array import Array
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.path.compounds.Vector2 import Vector2
from generated.formats.path.compounds.Vector3 import Vector3


class SupportSetRoot(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
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
		super().set_defaults()
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
		self.connector_1 = ArrayPointer(self.context, self.num_connector_1, generated.formats.path.compounds.Connector.Connector)
		self.connector_2 = ArrayPointer(self.context, self.num_connector_2, generated.formats.path.compounds.ConnectorMultiJoint.ConnectorMultiJoint)
		self.pillar = Pointer(self.context, 0, generated.formats.path.compounds.Pillar.Pillar)
		self.footer = Pointer(self.context, 0, generated.formats.path.compounds.Footer.Footer)
		self.data = ArrayPointer(self.context, self.num_data, generated.formats.path.compounds.SupportSetData.SupportSetData)

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
		instance.connector_1 = ArrayPointer.from_stream(stream, instance.context, instance.num_connector_1, generated.formats.path.compounds.Connector.Connector)
		instance.connector_2 = ArrayPointer.from_stream(stream, instance.context, instance.num_connector_2, generated.formats.path.compounds.ConnectorMultiJoint.ConnectorMultiJoint)
		instance.pillar = Pointer.from_stream(stream, instance.context, 0, generated.formats.path.compounds.Pillar.Pillar)
		instance.footer = Pointer.from_stream(stream, instance.context, 0, generated.formats.path.compounds.Footer.Footer)
		instance.padding = stream.read_uint64()
		instance.unk_vector_1 = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_vector_2 = Vector2.from_stream(stream, instance.context, 0, None)
		instance.unk_vector_3 = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_int_1 = stream.read_uint()
		instance.num_connector_1 = stream.read_uint()
		instance.num_connector_2 = stream.read_uint()
		instance.unk_ints = stream.read_uints((7,))
		instance.padding_2 = stream.read_uint64()
		instance.data = ArrayPointer.from_stream(stream, instance.context, instance.num_data, generated.formats.path.compounds.SupportSetData.SupportSetData)
		instance.num_data = stream.read_uint()
		if not isinstance(instance.connector_1, int):
			instance.connector_1.arg = instance.num_connector_1
		if not isinstance(instance.connector_2, int):
			instance.connector_2.arg = instance.num_connector_2
		if not isinstance(instance.pillar, int):
			instance.pillar.arg = 0
		if not isinstance(instance.footer, int):
			instance.footer.arg = 0
		if not isinstance(instance.data, int):
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
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('connector_1', ArrayPointer, (instance.num_connector_1, generated.formats.path.compounds.Connector.Connector))
		yield ('connector_2', ArrayPointer, (instance.num_connector_2, generated.formats.path.compounds.ConnectorMultiJoint.ConnectorMultiJoint))
		yield ('pillar', Pointer, (0, generated.formats.path.compounds.Pillar.Pillar))
		yield ('footer', Pointer, (0, generated.formats.path.compounds.Footer.Footer))
		yield ('padding', Uint64, (0, None))
		yield ('unk_vector_1', Vector3, (0, None))
		yield ('unk_vector_2', Vector2, (0, None))
		yield ('unk_vector_3', Vector3, (0, None))
		yield ('unk_int_1', Uint, (0, None))
		yield ('num_connector_1', Uint, (0, None))
		yield ('num_connector_2', Uint, (0, None))
		yield ('unk_ints', Array, ((7,), Uint, 0, None))
		yield ('padding_2', Uint64, (0, None))
		yield ('data', ArrayPointer, (instance.num_data, generated.formats.path.compounds.SupportSetData.SupportSetData))
		yield ('num_data', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'SupportSetRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* connector_1 = {self.fmt_member(self.connector_1, indent+1)}'
		s += f'\n	* connector_2 = {self.fmt_member(self.connector_2, indent+1)}'
		s += f'\n	* pillar = {self.fmt_member(self.pillar, indent+1)}'
		s += f'\n	* footer = {self.fmt_member(self.footer, indent+1)}'
		s += f'\n	* padding = {self.fmt_member(self.padding, indent+1)}'
		s += f'\n	* unk_vector_1 = {self.fmt_member(self.unk_vector_1, indent+1)}'
		s += f'\n	* unk_vector_2 = {self.fmt_member(self.unk_vector_2, indent+1)}'
		s += f'\n	* unk_vector_3 = {self.fmt_member(self.unk_vector_3, indent+1)}'
		s += f'\n	* unk_int_1 = {self.fmt_member(self.unk_int_1, indent+1)}'
		s += f'\n	* num_connector_1 = {self.fmt_member(self.num_connector_1, indent+1)}'
		s += f'\n	* num_connector_2 = {self.fmt_member(self.num_connector_2, indent+1)}'
		s += f'\n	* unk_ints = {self.fmt_member(self.unk_ints, indent+1)}'
		s += f'\n	* padding_2 = {self.fmt_member(self.padding_2, indent+1)}'
		s += f'\n	* data = {self.fmt_member(self.data, indent+1)}'
		s += f'\n	* num_data = {self.fmt_member(self.num_data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
