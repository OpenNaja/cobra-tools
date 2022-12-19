import os

from generated.formats.base.basic import Uint
from generated.formats.ovl.compounds.HeaderPointer import HeaderPointer
from generated.formats.ovl.compounds.NamedEntry import NamedEntry
from generated.formats.ovl_base.basic import OffsetString


class DependencyEntry(NamedEntry):

	"""
	Description of dependency; links it to an entry from this archive
	"""

	__name__ = 'DependencyEntry'

	_import_key = 'ovl.compounds.DependencyEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Hash of this dependency, for lookup in hash dict. Can be either external or internal.
		self.file_hash = 0

		# these use : instead of . at the start, eg. :tex
		self.ext_raw = 0

		# index into ovl file table, points to the file entry where this dependency is used
		self.file_index = 0

		# pointer into flattened list of all archives' pools
		self.link_ptr = HeaderPointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = NamedEntry._attribute_list + [
		('file_hash', Uint, (0, None), (False, None), None),
		('ext_raw', OffsetString, (None, None), (False, None), None),
		('file_index', Uint, (0, None), (False, None), None),
		('link_ptr', HeaderPointer, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'file_hash', Uint, (0, None), (False, None)
		yield 'ext_raw', OffsetString, (instance.context.names, None), (False, None)
		yield 'file_index', Uint, (0, None), (False, None)
		yield 'link_ptr', HeaderPointer, (0, None), (False, None)

	@property
	def ext(self):
		return self.ext_raw.replace(":", ".")

	@ext.setter
	def ext(self, e):
		self.ext_raw = e.replace(".", ":")

