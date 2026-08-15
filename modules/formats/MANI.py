import logging
import os
import struct

from generated.formats.manis.structs.ManisRoot import ManisRoot
from generated.formats.manis import ManisFile
from generated.formats.ovl import is_dla
from modules.formats.BaseFormat import BaseFile, MemStructLoader
from modules.formats.shared import get_padding
from modules.helpers import as_bytes


class ManiLoader(BaseFile):
	extension = ".mani"
	can_extract = False

	def create(self, file_path):
		self.root_ptr = (None, 0)


class ManiContext:
	def __init__(self):
		self.version = 260
		self.mani_version = 260


class ManisLoader(MemStructLoader):
	extension = ".manis"
	target_class = ManisRoot
				
	def extract(self, out_dir):
		name = self.name
		if not self.data_entry:
			raise AttributeError(f"No data entry for {name}")

		self.get_version()
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(struct.pack("<HHI", self.context.version, self.context.mani_version, len(self.children)))
			# store external datastream name
			ovs_name = [o for o in self.data_entries if o != "STATIC"][0] if len(self.data_entries) > 1 else ""
			outfile.write(as_bytes(ovs_name))
			for mani in self.children:
				outfile.write(as_bytes(mani.basename))
			# root gives general info
			outfile.write(as_bytes(self.header))
			for i, buff in enumerate(self.data_entry.buffers):
				outfile.write(buff.data)
				# buffer 0 - all mani infos
				# buffer 1 - list of hashes and zstrs for each bone name
				# buffer 2 - actual keys
				logging.debug(f"Buffer {i} len {len(buff.data)}")
				if i == 0:
					if self.mime_version <= 257:
						logging.debug(f"Added padding to buffer 0")
						outfile.write(get_padding(len(buff.data), 304))
					elif self.mime_version == 258:
						logging.debug(f"Added padding to buffer 0")
						outfile.write(get_padding(len(buff.data), 288))
				# if i == 1:
				# 	logging.debug(f"Added padding to buffer 1")
				# 	outfile.write(get_padding(len(buff.data), 4))
			# JWE2 can now have a secondary data entry holding a buffer 2 in an ovs
			for ovs_name, ext_data in self.data_entries.items():
				if ovs_name != "STATIC":
					logging.debug(f"Extracting from {ovs_name}")
					for buff in ext_data.buffers:
						outfile.write(buff.data)
	
		# for i, buff in enumerate(self.data_entry.buffers):
		# 	with open(out_path+str(i), 'wb') as outfile:
		# 		outfile.write(buff.data)
	
		return out_path,

	def get_version(self):
		self.context = ManiContext()
		self.context.version = self.mime_version
		if is_dla(self.ovl):
			self.context.version = 256
		self.context.mani_version = self.children[0].mime_version

	def collect(self):
		self.get_version()
		pool, offset = self.root_ptr
		stream = pool.stream_at(offset)
		self.header = self.target_class.from_stream(stream, self.context)

	def create(self, file_path):
		manis_file, root_data, b0, b1, b2, externals = self._get_data(file_path)
		ms2_dir = os.path.dirname(file_path)
		self.header = manis_file.header
		# create mani files
		for mani_barename in manis_file.names:
			mani_name = f"{mani_barename}.mani"
			mani_path = os.path.join(ms2_dir, mani_name)
			mani_loader = self.ovl.create_file(mani_path, mani_name)
			self.children.append(mani_loader)

		self.write_root_bytes(root_data)
		if externals:
			# JWE3: the ACL database bulk lives in paired LOD streams, so the static
			# entry keeps its three buffers and each tier gets its own data entry
			self.create_data_entry((b0, b1, b2))
			for ovs_name, blob in externals:
				self.create_data_entry((None, None, blob), ovs_name=ovs_name)
		elif manis_file.stream:
			self.create_data_entry((b0, b1, b""))
			self.create_data_entry((None, None, b2), ovs_name=manis_file.stream)
		else:
			self.create_data_entry((b0, b1, b2))

	def _get_data(self, file_path):
		"""Loads and returns the data for a manis"""
		manis_file = ManisFile()
		manis_file.load(file_path)
		# update mime version before writing to binary
		manis_file.version = manis_file.context.version = self.mime_version
		externals = self._split_external_buffers(file_path, manis_file)
		root_data = as_bytes(manis_file.header)
		raw_static = self._raw_static_buffers(file_path, manis_file, root_data)
		if raw_static is not None:
			b0, b1, b2 = raw_static
		else:
			b0 = as_bytes(manis_file.mani_infos)
			b1 = as_bytes(manis_file.name_buffer)
			b2 = as_bytes(manis_file.keys_buffer)
		return manis_file, root_data, b0, b1, b2, externals

	def _raw_static_buffers(self, file_path, manis_file, root_data):
		"""Slice the three static buffers straight out of the .manis, or None.

		Re-serialising from the parsed structures silently drops anything the schema
		does not model: the ACL compressed_database blob (240 bytes, inside buffer 0)
		and KeysReader's preserved inter-block auxiliary data (~2.5 KB, inside buffer
		2). Both are needed for JWE3 animation to survive a rebuild, so take the
		bytes verbatim and only fall back to re-serialising if the layout does not
		match what we expect.
		"""
		from source.formats.manis.database import locate_bulk
		with open(file_path, "rb") as f:
			raw = f.read()
		# extract() writes: <HHI> + ovs_name + one zstr per mani + root header + buffers
		preamble = 8 + len(as_bytes(str(manis_file.stream or "")))
		for mani_barename in manis_file.names:
			preamble += len(as_bytes(str(mani_barename)))
		preamble += len(root_data)
		# buffer 1 round-trips exactly, so it anchors the b0/b1 boundary
		b1 = as_bytes(manis_file.name_buffer)
		b1_start = raw.find(b1, preamble)
		if b1_start == -1:
			logging.warning(f"{self.name}: could not locate the name buffer, "
							f"falling back to re-serialised buffers")
			return None
		found = locate_bulk(raw)
		static_end = found["low_offset"] if found else len(raw)
		if not preamble < b1_start < static_end:
			logging.warning(f"{self.name}: unexpected buffer layout, "
							f"falling back to re-serialised buffers")
			return None
		return raw[preamble:b1_start], b1, raw[b1_start + len(b1):static_end]

	def _split_external_buffers(self, file_path, manis_file):
		"""Return [(ovs_name, data), ...] for the trailing ACL database bulk.

		JWE3 strips per-frame detail into an ACL database whose bulk data ships in
		paired LOD streams. extract() appends them to the .manis as
		[...][low tier][medium tier]EOF, and cobra stores the low tier in the _L0
		data entry and the medium tier in _L1. Without this they are silently
		dropped on rebuild and every clip in the bundle imports ~10x too stiff.
		"""
		from source.formats.manis.database import read_bulk_info, locate_bulk
		with open(file_path, "rb") as f:
			raw = f.read()
		info = read_bulk_info(raw)
		if info is None:
			return []
		found = locate_bulk(raw)
		if found is None:
			logging.warning(f"{self.name} has an ACL database but its bulk data was not "
							f"located; the rebuilt file will lose per-frame detail")
			return []
		low = raw[found["low_offset"]:found["low_offset"] + info["low_size"]]
		med = raw[found["medium_offset"]:found["medium_offset"] + info["medium_size"]]
		# manis_file.stream holds the first non-STATIC entry name written by extract,
		# eg. 'Anim_L0' or 'Anim_Hunting_L0'; strip the tier suffix to get the base
		stream = str(manis_file.stream or "Anim_L0")
		base = stream[:-3] if stream.endswith(("_L0", "_L1")) else stream
		return [(f"{base}_L0", low), (f"{base}_L1", med)]
