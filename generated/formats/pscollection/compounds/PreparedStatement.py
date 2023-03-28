from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PreparedStatement(MemStruct):

	__name__ = 'PreparedStatement'

	_import_key = 'pscollection.compounds.PreparedStatement'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.arg_count = 0
		self.args = ArrayPointer(self.context, self.arg_count, PreparedStatement._import_map["pscollection.compounds.Arg"])
		self.statement_name = Pointer(self.context, 0, ZString)
		self.sql_query = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('args', ArrayPointer, (None, PreparedStatement._import_map["pscollection.compounds.Arg"]), (False, None), (None, None))
		yield ('arg_count', Uint64, (0, None), (True, 0), (None, None))
		yield ('statement_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('sql_query', Pointer, (0, ZString), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'args', ArrayPointer, (instance.arg_count, PreparedStatement._import_map["pscollection.compounds.Arg"]), (False, None)
		yield 'arg_count', Uint64, (0, None), (True, 0)
		yield 'statement_name', Pointer, (0, ZString), (False, None)
		yield 'sql_query', Pointer, (0, ZString), (False, None)


PreparedStatement.init_attributes()
