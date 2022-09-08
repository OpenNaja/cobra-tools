

import logging

from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class BufferEntry(BaseStruct):

	"""
	8 bytes
	"""

	__name__ = 'BufferEntry'

	_import_path = 'generated.formats.ovl.compounds.BufferEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index of buffer in file; id from sorting of data entries
		self.index = 0

		# in bytes
		self.size = 0

		# id; index is taken from buffer group
		self.file_hash = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		if self.context.version <= 19:
			self.index = 0
		self.size = 0
		if self.context.version >= 20:
			self.file_hash = 0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 19:
			yield 'index', Uint, (0, None), (False, None)
		yield 'size', Uint, (0, None), (False, None)
		if instance.context.version >= 20:
			yield 'file_hash', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BufferEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def read_data(self, stream):
		"""Load data from archive stream into self for modification and io"""
		self.data = stream.read(self.size)

	def update_data(self, data):
		"""Set data internal data so it can be written on save and update the size value"""
		self.data = data
		self.size = len(data)

	def __eq__(self, other):
		attr_check = ("index", "size", "file_hash")
		same = True
		for attr in attr_check:
			a = getattr(self, attr)
			b = getattr(other, attr)
			if a != b:
				logging.warning(f"Buffer differs for '{attr}' - {a} vs {b}")
				same = False
		return same

