from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Driver(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'Driver'

	_import_key = 'posedriverdef.compounds.Driver'

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
		self.data = Pointer(self.context, 0, Driver._import_map["posedriverdef.compounds.Data"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'joint_name', Pointer, (0, ZString), (False, None)
		yield 'a', Ubyte, (0, None), (False, None)
		yield 'b', Ubyte, (0, None), (False, None)
		yield 'c', Ushort, (0, None), (False, None)
		yield 'd', Uint, (0, None), (False, None)
		yield 'driven_joint_name', Pointer, (0, ZString), (False, None)
		yield 'unk_1', Uint64, (0, None), (False, None)
		yield 'data', Pointer, (0, Driver._import_map["posedriverdef.compounds.Data"]), (False, None)
		yield 'unk_2', Uint64, (0, None), (False, None)
