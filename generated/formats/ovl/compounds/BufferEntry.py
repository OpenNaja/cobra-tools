
import logging

from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class BufferEntry(BaseStruct):

	"""
	8 bytes
	"""

	__name__ = 'BufferEntry'

	_import_key = 'ovl.compounds.BufferEntry'

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

	_attribute_list = BaseStruct._attribute_list + [
		('index', Uint, (0, None), (False, None), True),
		('size', Uint, (0, None), (False, None), None),
		('file_hash', Uint, (0, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 19:
			yield 'index', Uint, (0, None), (False, None)
		yield 'size', Uint, (0, None), (False, None)
		if instance.context.version >= 20:
			yield 'file_hash', Uint, (0, None), (False, None)

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

