from generated.formats.userinterfaceicondata.structs.UserinterfaceicondataRoot import UserinterfaceicondataRoot
from modules.formats.BaseFormat import MemStructLoader


class UserinterfaceicondataLoader(MemStructLoader):
	extension = ".userinterfaceicondata"
	target_class = UserinterfaceicondataRoot
