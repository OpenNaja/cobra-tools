from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Joint(MemStruct):

	__name__ = 'Joint'

	_import_key = 'path.compounds.Joint'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_float = 0.0
		self.unk_int = 0
		self.unk_int_2 = 0
		self.joint_1 = Pointer(self.context, 0, ZString)
		self.joint_2 = Pointer(self.context, 0, ZString)
		self.joint_3 = Pointer(self.context, 0, ZString)
		self.joint_4 = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('joint_1', Pointer, (0, ZString), (False, None), None)
		yield ('joint_2', Pointer, (0, ZString), (False, None), None)
		yield ('joint_3', Pointer, (0, ZString), (False, None), None)
		yield ('joint_4', Pointer, (0, ZString), (False, None), None)
		yield ('unk_float', Float, (0, None), (False, None), None)
		yield ('unk_int', Uint, (0, None), (False, None), None)
		yield ('unk_int_2', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'joint_1', Pointer, (0, ZString), (False, None)
		yield 'joint_2', Pointer, (0, ZString), (False, None)
		yield 'joint_3', Pointer, (0, ZString), (False, None)
		yield 'joint_4', Pointer, (0, ZString), (False, None)
		yield 'unk_float', Float, (0, None), (False, None)
		yield 'unk_int', Uint, (0, None), (False, None)
		yield 'unk_int_2', Uint64, (0, None), (False, None)


Joint.init_attributes()
