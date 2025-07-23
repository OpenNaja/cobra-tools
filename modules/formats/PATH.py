from generated.formats.path.compounds.PathExtrusion import PathExtrusion
from generated.formats.path.compounds.PathMaterial import PathMaterial
from generated.formats.path.compounds.PathResource import PathResource
from generated.formats.path.compounds.PathSupport import PathSupport
from generated.formats.path.compounds.PathType import PathType
from generated.formats.path.compounds.SupportSetRoot import SupportSetRoot
from generated.formats.path.compounds.LatticeSupportSetRoot import LatticeSupportSetRoot
from generated.formats.path.compounds.WoodenSupportSetRoot import WoodenSupportSetRoot
from generated.formats.path.compounds.PathJoinPartResourceRoot import PathJoinPartResourceRoot
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
