from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Arg(MemStruct):

	__name__ = 'Arg'

	_import_key = 'pscollection.compounds.Arg'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.arg_type = 0

		# one-based index
		self.arg_index = 0
		self.u_1 = 0
		self.u_2 = 0
		self.u_3 = 0
		self.u_4 = 0
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('u_0', Ubyte, (0, None), (False, None), None),
		('arg_type', Ubyte, (0, None), (False, None), None),
		('arg_index', Ubyte, (0, None), (False, None), None),
		('u_1', Ubyte, (0, None), (False, None), None),
		('u_2', Uint, (0, None), (False, None), None),
		('u_3', Uint64, (0, None), (False, None), None),
		('u_4', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_0', Ubyte, (0, None), (False, None)
		yield 'arg_type', Ubyte, (0, None), (False, None)
		yield 'arg_index', Ubyte, (0, None), (False, None)
		yield 'u_1', Ubyte, (0, None), (False, None)
		yield 'u_2', Uint, (0, None), (False, None)
		yield 'u_3', Uint64, (0, None), (False, None)
		yield 'u_4', Uint64, (0, None), (False, None)
