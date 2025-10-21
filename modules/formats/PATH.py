from generated.formats.path.structs.PathExtrusion import PathExtrusion
from generated.formats.path.structs.PathMaterial import PathMaterial
from generated.formats.path.structs.PathResource import PathResource
from generated.formats.path.structs.PathSupport import PathSupport
from generated.formats.path.structs.PathType import PathType
from generated.formats.path.structs.SupportSetRoot import SupportSetRoot
from generated.formats.path.structs.LatticeSupportSetRoot import LatticeSupportSetRoot
from generated.formats.path.structs.WoodenSupportSetRoot import WoodenSupportSetRoot
from generated.formats.path.structs.PathJoinPartResourceRoot import PathJoinPartResourceRoot
from modules.formats.BaseFormat import MemStructLoader, MimeVersionedLoader


class PathExtrusionLoader(MemStructLoader):
	target_class = PathExtrusion
	extension = ".pathextrusion"


class PathMaterialLoader(MemStructLoader):
	target_class = PathMaterial
	extension = ".pathmaterial"


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


class SupportSetLoader(MimeVersionedLoader):
	target_class = SupportSetRoot
	extension = ".supportset"


class LatticeSupportSetLoader(MemStructLoader):
	target_class = LatticeSupportSetRoot
	extension = ".latticesupportset"


class WoodenSupportSetLoader(MemStructLoader):
	target_class = WoodenSupportSetRoot
	extension = ".woodensupportset"
