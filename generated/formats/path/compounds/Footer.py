import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Footer(MemStruct):

	__name__ = 'Footer'

	_import_key = 'path.compounds.Footer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_int = 0
		self.unk_floats = Array(self.context, 0, None, (0,), Float)
		self.footer_piece = Pointer(self.context, 0, ZString)
		self.joint = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('footer_piece', Pointer, (0, ZString), (False, None), None),
		('unk_int', Uint64, (0, None), (False, None), None),
		('joint', Pointer, (0, ZString), (False, None), None),
		('unk_floats', Array, (0, None, (2,), Float), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'footer_piece', Pointer, (0, ZString), (False, None)
		yield 'unk_int', Uint64, (0, None), (False, None)
		yield 'joint', Pointer, (0, ZString), (False, None)
		yield 'unk_floats', Array, (0, None, (2,), Float), (False, None)
