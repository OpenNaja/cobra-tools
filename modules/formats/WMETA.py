from generated.formats.wmeta.structs.WmetasbRoot import WmetasbRoot
from modules.formats.BaseFormat import MemStructLoader, MimeVersionedLoader


class WmetaLoader(MimeVersionedLoader):
	target_class = WmetasbRoot
	extension = ".wmetasb"

