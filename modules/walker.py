import os
import io
import tempfile
import shutil

from pyffi_ext.formats.dds import DdsFormat
from pyffi_ext.formats.ms2 import Ms2Format
# from pyffi_ext.formats.bani import BaniFormat
# from pyffi_ext.formats.ovl import OvlFormat
from pyffi_ext.formats.fgm import FgmFormat
from pyffi_ext.formats.materialcollection import MaterialcollectionFormat
# from pyffi_ext.formats.assetpkg import AssetpkgFormat
from pyffi_ext.formats.ovl import OvlFormat


def walk_type(start_dir, extension="ovl"):
	print(f"Scanning {start_dir} for {extension} files")
	ret = []
	for root, dirs, files in os.walk(start_dir, topdown=False):
		for name in files:
			if name.lower().endswith("."+extension):
				ret.append(os.path.join(root, name))
	return ret

