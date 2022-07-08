from generated.formats.path.compound.PathExtrusion import PathExtrusion
from generated.formats.path.compound.PathMaterial import PathMaterial
from generated.formats.path.compound.PathResource import PathResource
from generated.formats.path.compound.PathSupport import PathSupport
from generated.formats.path.compound.PathType import PathType
from generated.formats.path.compound.SupportSetRoot import SupportSetRoot
from generated.formats.path.compound.PathJoinPartResourceRoot import PathJoinPartResourceRoot
from modules.formats.BaseFormat import MemStructLoader


class PathExtrusionLoader(MemStructLoader):
	target_class = PathExtrusion
	extension = ".pathextrusion"

class PathMaterialLoader(MemStructLoader):
	target_class = PathMaterial
	extension = ".pathmaterial"

	def prep(self):
		# avoid generating pointers for these
		if not self.header.num_data:
			self.header.mat_data.data = None

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		self.prep()
		# print(self.header)
		self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)

class PathResourceLoader(MemStructLoader):
	target_class = PathResource
	extension = ".pathresource"

class PathJoinPartResourceLoader(MemStructLoader):
	target_class = PathJoinPartResourceRoot
	extension = ".pathjoinpartresource"

class PathSupportLoader(MemStructLoader):
	target_class = PathSupport
	extension = ".pathsupport"

class PathTypeLoader(MemStructLoader):
	target_class = PathType
	extension = ".pathtype"

class SupportSetLoader(MemStructLoader):
	target_class = SupportSetRoot
	extension = ".supportset"
