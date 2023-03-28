from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PscollectionRoot(MemStruct):

	__name__ = 'PscollectionRoot'

	_import_key = 'pscollection.compounds.PscollectionRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.prepared_statements = ArrayPointer(self.context, self.count, PscollectionRoot._import_map["pscollection.compounds.PreparedStatement"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('prepared_statements', ArrayPointer, (None, PscollectionRoot._import_map["pscollection.compounds.PreparedStatement"]), (False, None), (None, None))
		yield ('count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'prepared_statements', ArrayPointer, (instance.count, PscollectionRoot._import_map["pscollection.compounds.PreparedStatement"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)


PscollectionRoot.init_attributes()
