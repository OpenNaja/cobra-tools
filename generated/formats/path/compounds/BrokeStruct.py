from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.path.compounds.Vector3 import Vector3


class BrokeStruct(MemStruct):

	__name__ = 'BrokeStruct'

	_import_key = 'path.compounds.BrokeStruct'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_vector_1 = Vector3(self.context, 0, None)
		self.unk_vector_2 = Vector3(self.context, 0, None)
		self.support = Pointer(self.context, 0, ZString)
		self.fallen_support = Pointer(self.context, 0, ZString)
		self.head = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('support', Pointer, (0, ZString), (False, None), (None, None))
		yield ('fallen_support', Pointer, (0, ZString), (False, None), (None, None))
		yield ('head', Pointer, (0, ZString), (False, None), (None, None))
		yield ('unk_vector_1', Vector3, (0, None), (False, None), (None, None))
		yield ('unk_vector_2', Vector3, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'support', Pointer, (0, ZString), (False, None)
		yield 'fallen_support', Pointer, (0, ZString), (False, None)
		yield 'head', Pointer, (0, ZString), (False, None)
		yield 'unk_vector_1', Vector3, (0, None), (False, None)
		yield 'unk_vector_2', Vector3, (0, None), (False, None)


BrokeStruct.init_attributes()
