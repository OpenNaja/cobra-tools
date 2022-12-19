import os

from generated.base_struct import BaseStruct


class NamedEntry(BaseStruct):

	"""
	name is stored in basename and ext attributes
	"""

	__name__ = 'NamedEntry'

	_import_key = 'ovl.compounds.NamedEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	@property
	def name(self):
		return self.basename + self.ext

	@name.setter
	def name(self, n):
		self.basename, self.ext = os.path.splitext(n)

