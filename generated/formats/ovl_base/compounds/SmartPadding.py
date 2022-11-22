from generated.io import MAX_LEN

ZERO = b"\x00"


from generated.base_struct import BaseStruct


class SmartPadding(BaseStruct):

	"""
	Grabs 00 bytes only
	"""

	__name__ = 'SmartPadding'

	_import_key = 'ovl_base.compounds.SmartPadding'

	_attribute_list = BaseStruct._attribute_list + [
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""

	def __repr__(self):
		return f"{self.data} Size: {len(self.data)}"

	@classmethod
	def read_fields(cls, stream, instance):
		instance.data = b''
		if instance.arg is None:
			raster = 1
		else:
			raster = instance.arg
		for i in range(MAX_LEN):
			end = stream.tell()
			chars = stream.read(raster)
			# stop if a byte other than 00 is encountered
			if chars != ZERO * raster:
				break
			# it's 00 so add it to the padding
			instance.data += chars
		else:
			raise ValueError('padding too long')
		stream.seek(end)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write(instance.data)


