from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ConnectorMultiJoint(MemStruct):

	__name__ = 'ConnectorMultiJoint'

	_import_key = 'path.compounds.ConnectorMultiJoint'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.padding = 0
		self.num_joints = 0
		self.unk_float_1 = 0.0
		self.unk_float_2 = 0.0
		self.unk_int_1 = 0
		self.model_name = Pointer(self.context, 0, ZString)
		self.joints = ArrayPointer(self.context, self.num_joints, ConnectorMultiJoint._import_map["path.compounds.Joint"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('model_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('padding', Uint64, (0, None), (False, 0), (None, None))
		yield ('joints', ArrayPointer, (None, ConnectorMultiJoint._import_map["path.compounds.Joint"]), (False, None), (None, None))
		yield ('num_joints', Uint, (0, None), (False, None), (None, None))
		yield ('unk_float_1', Float, (0, None), (False, None), (None, None))
		yield ('unk_float_2', Float, (0, None), (False, None), (None, None))
		yield ('unk_int_1', Uint, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'model_name', Pointer, (0, ZString), (False, None)
		yield 'padding', Uint64, (0, None), (False, 0)
		yield 'joints', ArrayPointer, (instance.num_joints, ConnectorMultiJoint._import_map["path.compounds.Joint"]), (False, None)
		yield 'num_joints', Uint, (0, None), (False, None)
		yield 'unk_float_1', Float, (0, None), (False, None)
		yield 'unk_float_2', Float, (0, None), (False, None)
		yield 'unk_int_1', Uint, (0, None), (False, None)
