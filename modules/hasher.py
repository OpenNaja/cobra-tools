import struct
import os
import io
import tempfile
import shutil

from pyffi_ext.formats.dds import DdsFormat
from pyffi_ext.formats.ms2 import Ms2Format
from pyffi_ext.formats.bani import BaniFormat
from pyffi_ext.formats.ovl import OvlFormat
from pyffi_ext.formats.fgm import FgmFormat
from pyffi_ext.formats.materialcollection import MaterialcollectionFormat

from modules import extract
from util import texconv, imarray

def djbb(s):
	# calculates DJB hash for string s
	# from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
	hash = 5381
	for x in s:
		hash = (( hash << 5) + hash) + ord(x)
	return hash & 0xFFFFFFFF

def dat_hasher(archive):
	print("\nHashing from archive",archive.archive_index)
	for sized_str_entry in archive.header_entries:
		new_name = sized_str_entry.name
		new_name[0] = "z"
		new_hash = djbb(new_name)
		print(sized_str_entry.name,sized_str_entry.file_hash,new_name,new_hash)
		sized_str_entry.file_hash = new_hash
	for data_entry in archive.data_entries:
		new_name = data_entry.name
		new_name[0] = "z"
		new_hash = djbb(new_name)
		data_entry.file_hash = new_hash
	for set_entry in archive.set_header.sets:
		new_name = set_entry.name
		new_name[0] = "z"
		new_hash = djbb(new_name)
		set_entry.file_hash = new_hash
	for asset_entry in archive.set_header.assets:
		new_name = asset_entry.name
		new_name[0] = "z"
		new_hash = djbb(new_name)
		asset_entry.file_hash = new_hash
	print("/nDone!")
	
	

