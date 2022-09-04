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

	__name__ = 'SupportSetRoot'

	_import_path = 'generated.formats.path.compounds.SupportSetRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.padding = 0
		self.unk_vector_1 = Vector3(self.context, 0, None)
		self.unk_vector_2 = Vector2(self.context, 0, None)
		self.unk_vector_3 = Vector3(self.context, 0, None)
		self.unk_int_1 = 0
		self.num_connector_1 = 0
		self.num_connector_2 = 0
		self.unk_ints = Array(self.context, 0, None, (0,), Uint)
		self.padding_2 = 0
		self.num_data = 0
		self.connector_1 = ArrayPointer(self.context, self.num_connector_1, SupportSetRoot._import_path_map["generated.formats.path.compounds.Connector"])
		self.connector_2 = ArrayPointer(self.context, self.num_connector_2, SupportSetRoot._import_path_map["generated.formats.path.compounds.ConnectorMultiJoint"])
		self.pillar = Pointer(self.context, 0, SupportSetRoot._import_path_map["generated.formats.path.compounds.Pillar"])
		self.footer = Pointer(self.context, 0, SupportSetRoot._import_path_map["generated.formats.path.compounds.Footer"])
		self.data = ArrayPointer(self.context, self.num_data, SupportSetRoot._import_path_map["generated.formats.path.compounds.SupportSetData"])
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
		self.connector_1 = ArrayPointer(self.context, self.num_connector_1, SupportSetRoot._import_path_map["generated.formats.path.compounds.Connector"])
		self.connector_2 = ArrayPointer(self.context, self.num_connector_2, SupportSetRoot._import_path_map["generated.formats.path.compounds.ConnectorMultiJoint"])
		self.pillar = Pointer(self.context, 0, SupportSetRoot._import_path_map["generated.formats.path.compounds.Pillar"])
		self.footer = Pointer(self.context, 0, SupportSetRoot._import_path_map["generated.formats.path.compounds.Footer"])
		self.data = ArrayPointer(self.context, self.num_data, SupportSetRoot._import_path_map["generated.formats.path.compounds.SupportSetData"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.connector_1 = ArrayPointer.from_stream(stream, instance.context, instance.num_connector_1, SupportSetRoot._import_path_map["generated.formats.path.compounds.Connector"])
		instance.connector_2 = ArrayPointer.from_stream(stream, instance.context, instance.num_connector_2, SupportSetRoot._import_path_map["generated.formats.path.compounds.ConnectorMultiJoint"])
		instance.pillar = Pointer.from_stream(stream, instance.context, 0, SupportSetRoot._import_path_map["generated.formats.path.compounds.Pillar"])
		instance.footer = Pointer.from_stream(stream, instance.context, 0, SupportSetRoot._import_path_map["generated.formats.path.compounds.Footer"])
		instance.padding = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_vector_1 = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_vector_2 = Vector2.from_stream(stream, instance.context, 0, None)
		instance.unk_vector_3 = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_int_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_connector_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_connector_2 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_ints = Array.from_stream(stream, instance.context, 0, None, (7,), Uint)
		instance.padding_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data = ArrayPointer.from_stream(stream, instance.context, instance.num_data, SupportSetRoot._import_path_map["generated.formats.path.compounds.SupportSetData"])
		instance.num_data = Uint.from_stream(stream, instance.context, 0, None)
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
		Uint64.to_stream(stream, instance.padding)
		Vector3.to_stream(stream, instance.unk_vector_1)
		Vector2.to_stream(stream, instance.unk_vector_2)
		Vector3.to_stream(stream, instance.unk_vector_3)
		Uint.to_stream(stream, instance.unk_int_1)
		Uint.to_stream(stream, instance.num_connector_1)
		Uint.to_stream(stream, instance.num_connector_2)
		Array.to_stream(stream, instance.unk_ints, instance.context, 0, None, (7,), Uint)
		Uint64.to_stream(stream, instance.padding_2)
		ArrayPointer.to_stream(stream, instance.data)
		Uint.to_stream(stream, instance.num_data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'connector_1', ArrayPointer, (instance.num_connector_1, SupportSetRoot._import_path_map["generated.formats.path.compounds.Connector"]), (False, None)
		yield 'connector_2', ArrayPointer, (instance.num_connector_2, SupportSetRoot._import_path_map["generated.formats.path.compounds.ConnectorMultiJoint"]), (False, None)
		yield 'pillar', Pointer, (0, SupportSetRoot._import_path_map["generated.formats.path.compounds.Pillar"]), (False, None)
		yield 'footer', Pointer, (0, SupportSetRoot._import_path_map["generated.formats.path.compounds.Footer"]), (False, None)
		yield 'padding', Uint64, (0, None), (True, 0)
		yield 'unk_vector_1', Vector3, (0, None), (False, None)
		yield 'unk_vector_2', Vector2, (0, None), (False, None)
		yield 'unk_vector_3', Vector3, (0, None), (False, None)
		yield 'unk_int_1', Uint, (0, None), (False, None)
		yield 'num_connector_1', Uint, (0, None), (False, None)
		yield 'num_connector_2', Uint, (0, None), (False, None)
		yield 'unk_ints', Array, (0, None, (7,), Uint), (False, None)
		yield 'padding_2', Uint64, (0, None), (True, 0)
		yield 'data', ArrayPointer, (instance.num_data, SupportSetRoot._import_path_map["generated.formats.path.compounds.SupportSetData"]), (False, None)
		yield 'num_data', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'SupportSetRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
