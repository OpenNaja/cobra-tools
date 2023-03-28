import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.path.compounds.Vector2 import Vector2
from generated.formats.path.compounds.Vector3 import Vector3


class SupportSetRoot(MemStruct):

	__name__ = 'SupportSetRoot'

	_import_key = 'path.compounds.SupportSetRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_vector_1 = Vector3(self.context, 0, None)
		self.unk_vector_2 = Vector2(self.context, 0, None)
		self.unk_vector_3 = Vector3(self.context, 0, None)
		self.unk_int_1 = 0
		self.num_connector_1 = 0
		self.num_connector_2 = 0
		self.num_pillar = 0
		self.num_subbrace = 0
		self.num_broken_support = 0
		self.unk_floats = Array(self.context, 0, None, (0,), Float)
		self.num_data = 0
		self.zeros = Array(self.context, 0, None, (0,), Uint)
		self.connector_1 = ArrayPointer(self.context, self.num_connector_1, SupportSetRoot._import_map["path.compounds.Connector"])
		self.connector_2 = ArrayPointer(self.context, self.num_connector_2, SupportSetRoot._import_map["path.compounds.ConnectorMultiJoint"])
		self.pillar = ArrayPointer(self.context, self.num_pillar, SupportSetRoot._import_map["path.compounds.Pillar"])
		self.footer = ArrayPointer(self.context, self.num_pillar, SupportSetRoot._import_map["path.compounds.Footer"])
		self.sub_braces = ArrayPointer(self.context, self.num_subbrace, SupportSetRoot._import_map["path.compounds.SubBraceStruct"])
		self.broken_supports = ArrayPointer(self.context, self.num_broken_support, SupportSetRoot._import_map["path.compounds.BrokeStruct"])
		self.data = ArrayPointer(self.context, self.num_data, SupportSetRoot._import_map["path.compounds.SupportSetData"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('connector_1', ArrayPointer, (None, SupportSetRoot._import_map["path.compounds.Connector"]), (False, None), (None, None))
		yield ('connector_2', ArrayPointer, (None, SupportSetRoot._import_map["path.compounds.ConnectorMultiJoint"]), (False, None), (None, None))
		yield ('pillar', ArrayPointer, (None, SupportSetRoot._import_map["path.compounds.Pillar"]), (False, None), (None, None))
		yield ('footer', ArrayPointer, (None, SupportSetRoot._import_map["path.compounds.Footer"]), (False, None), (None, None))
		yield ('sub_braces', ArrayPointer, (None, SupportSetRoot._import_map["path.compounds.SubBraceStruct"]), (False, None), (None, None))
		yield ('unk_vector_1', Vector3, (0, None), (False, None), (None, None))
		yield ('unk_vector_2', Vector2, (0, None), (False, None), (None, None))
		yield ('unk_vector_3', Vector3, (0, None), (False, None), (None, None))
		yield ('unk_int_1', Uint, (0, None), (False, None), (None, None))
		yield ('num_connector_1', Uint, (0, None), (False, None), (None, None))
		yield ('num_connector_2', Uint, (0, None), (False, None), (None, None))
		yield ('num_pillar', Uint, (0, None), (False, None), (None, None))
		yield ('num_subbrace', Uint, (0, None), (False, None), (None, None))
		yield ('num_broken_support', Uint, (0, None), (False, None), (None, None))
		yield ('unk_floats', Array, (0, None, (4,), Float), (False, None), (None, None))
		yield ('broken_supports', ArrayPointer, (None, SupportSetRoot._import_map["path.compounds.BrokeStruct"]), (False, None), (None, None))
		yield ('data', ArrayPointer, (None, SupportSetRoot._import_map["path.compounds.SupportSetData"]), (False, None), (None, None))
		yield ('num_data', Uint, (0, None), (False, None), (None, None))
		yield ('zeros', Array, (0, None, (3,), Uint), (False, 0), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'connector_1', ArrayPointer, (instance.num_connector_1, SupportSetRoot._import_map["path.compounds.Connector"]), (False, None)
		yield 'connector_2', ArrayPointer, (instance.num_connector_2, SupportSetRoot._import_map["path.compounds.ConnectorMultiJoint"]), (False, None)
		yield 'pillar', ArrayPointer, (instance.num_pillar, SupportSetRoot._import_map["path.compounds.Pillar"]), (False, None)
		yield 'footer', ArrayPointer, (instance.num_pillar, SupportSetRoot._import_map["path.compounds.Footer"]), (False, None)
		yield 'sub_braces', ArrayPointer, (instance.num_subbrace, SupportSetRoot._import_map["path.compounds.SubBraceStruct"]), (False, None)
		yield 'unk_vector_1', Vector3, (0, None), (False, None)
		yield 'unk_vector_2', Vector2, (0, None), (False, None)
		yield 'unk_vector_3', Vector3, (0, None), (False, None)
		yield 'unk_int_1', Uint, (0, None), (False, None)
		yield 'num_connector_1', Uint, (0, None), (False, None)
		yield 'num_connector_2', Uint, (0, None), (False, None)
		yield 'num_pillar', Uint, (0, None), (False, None)
		yield 'num_subbrace', Uint, (0, None), (False, None)
		yield 'num_broken_support', Uint, (0, None), (False, None)
		yield 'unk_floats', Array, (0, None, (4,), Float), (False, None)
		yield 'broken_supports', ArrayPointer, (instance.num_broken_support, SupportSetRoot._import_map["path.compounds.BrokeStruct"]), (False, None)
		yield 'data', ArrayPointer, (instance.num_data, SupportSetRoot._import_map["path.compounds.SupportSetData"]), (False, None)
		yield 'num_data', Uint, (0, None), (False, None)
		yield 'zeros', Array, (0, None, (3,), Uint), (False, 0)


SupportSetRoot.init_attributes()
