import typing
from generated.formats.matcol.compound.MaterialInfo import MaterialInfo


class VariantWrapper:
	info: MaterialInfo
	materials: typing.List[str]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = MaterialInfo()
		self.materials = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.info = stream.read_type(MaterialInfo)
		self.materials = [stream.read_zstring() for _ in range(self.info.material_count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.info)
		for item in self.materials: stream.write_zstring(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'VariantWrapper [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* info = ' + self.info.__repr__()
		s += '\n	* materials = ' + self.materials.__repr__()
		s += '\n'
		return s
