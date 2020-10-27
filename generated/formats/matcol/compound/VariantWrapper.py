import typing
from generated.array import Array
from generated.formats.matcol.compound.MaterialInfo import MaterialInfo


class VariantWrapper:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = MaterialInfo()
		self.materials = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.info = stream.read_type(MaterialInfo)
		self.materials.read(stream, 'ZString', self.info.material_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.info)
		self.materials.write(stream, 'ZString', self.info.material_count, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'VariantWrapper [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* info = ' + self.info.__repr__()
		s += '\n	* materials = ' + self.materials.__repr__()
		s += '\n'
		return s
