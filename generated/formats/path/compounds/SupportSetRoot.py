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

	_import_key = 'path.compounds.SupportSetRoot'

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
		self.connector_1 = ArrayPointer(self.context, self.num_connector_1, SupportSetRoot._import_map["path.compounds.Connector"])
		self.connector_2 = ArrayPointer(self.context, self.num_connector_2, SupportSetRoot._import_map["path.compounds.ConnectorMultiJoint"])
		self.pillar = Pointer(self.context, 0, SupportSetRoot._import_map["path.compounds.Pillar"])
		self.footer = Pointer(self.context, 0, SupportSetRoot._import_map["path.compounds.Footer"])
		self.data = ArrayPointer(self.context, self.num_data, SupportSetRoot._import_map["path.compounds.SupportSetData"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'connector_1', ArrayPointer, (instance.num_connector_1, SupportSetRoot._import_map["path.compounds.Connector"]), (False, None)
		yield 'connector_2', ArrayPointer, (instance.num_connector_2, SupportSetRoot._import_map["path.compounds.ConnectorMultiJoint"]), (False, None)
		yield 'pillar', Pointer, (0, SupportSetRoot._import_map["path.compounds.Pillar"]), (False, None)
		yield 'footer', Pointer, (0, SupportSetRoot._import_map["path.compounds.Footer"]), (False, None)
		yield 'padding', Uint64, (0, None), (True, 0)
		yield 'unk_vector_1', Vector3, (0, None), (False, None)
		yield 'unk_vector_2', Vector2, (0, None), (False, None)
		yield 'unk_vector_3', Vector3, (0, None), (False, None)
		yield 'unk_int_1', Uint, (0, None), (False, None)
		yield 'num_connector_1', Uint, (0, None), (False, None)
		yield 'num_connector_2', Uint, (0, None), (False, None)
		yield 'unk_ints', Array, (0, None, (7,), Uint), (False, None)
		yield 'padding_2', Uint64, (0, None), (True, 0)
		yield 'data', ArrayPointer, (instance.num_data, SupportSetRoot._import_map["path.compounds.SupportSetData"]), (False, None)
		yield 'num_data', Uint, (0, None), (False, None)
