from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ovl.compounds.NamedEntry import NamedEntry
from generated.formats.ovl_base.basic import OffsetString


class FileEntry(NamedEntry):

	"""
	Description of one file in the archive
	"""

	__name__ = 'FileEntry'

	_import_key = 'ovl.compounds.FileEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.basename = 0

		# this hash is used to retrieve the file name from inside the archive
		self.file_hash = 0

		# pool type of this file's root pointer, if part of a set, it's usually the same as set pool type
		self.pool_type = 0

		# if this file is part of a set, the set's root entry's pool type, else 0
		self.set_pool_type = 0

		# index into 'Extensions' array
		self.extension = 0
		if set_default:
			self.set_defaults()

	_attribute_list = NamedEntry._attribute_list + [
		('basename', OffsetString, (None, None), (False, None), None),
		('file_hash', Uint, (0, None), (False, None), None),
		('pool_type', Byte, (0, None), (False, None), None),
		('set_pool_type', Byte, (0, None), (False, None), None),
		('extension', Ushort, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'basename', OffsetString, (instance.context.names, None), (False, None)
		yield 'file_hash', Uint, (0, None), (False, None)
		yield 'pool_type', Byte, (0, None), (False, None)
		yield 'set_pool_type', Byte, (0, None), (False, None)
		yield 'extension', Ushort, (0, None), (False, None)

	def update_constants(self, ovl):
		"""Update the constants"""
		self.pool_type = ovl.get_mime(self.ext, "pool")
		self.set_pool_type = ovl.get_mime(self.ext, "set_pool")

