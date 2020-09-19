class HeaderPointer:

# Not standalone, used by SizedStringEntry and Fragment
# 8 bytes

	# The index of the HeaderEntry this one relates to; OR, for entries referred to from AssetEntries: 4294967295 (FF FF FF FF), uint32 max
	header_index: int

	# the start position of the sized string's size uint
	data_offset: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.header_index = stream.read_uint()
		self.data_offset = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.header_index)
		stream.write_uint(self.data_offset)

	def __repr__(self):
		s = 'HeaderPointer'
		s += '\nheader_index ' + self.header_index.__repr__()
		s += '\ndata_offset ' + self.data_offset.__repr__()
		s += '\n'
		return s