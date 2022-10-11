from generated.formats.physicssurfacesxmlres.compounds.PhysicsSurfaceXMLResRoot import PhysicsSurfaceXMLResRoot
from modules.formats.BaseFormat import MemStructLoader

class PhysicsSurfaceXMLResLoader(MemStructLoader):
	target_class = PhysicsSurfaceXMLResRoot
	extension = ".physicssurfacesxmlres"