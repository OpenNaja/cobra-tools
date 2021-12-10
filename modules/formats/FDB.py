import logging
import os
import shutil
import sqlite3
import struct

from generated.formats.ovl_base.versions import is_pz, is_pz16
from modules.formats.BaseFormat import BaseFile


class FdbLoader(BaseFile):

	def create(self):
		ss, buffer_0, buffer_1 = self._get_data(self.file_entry.path)
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		pool.data.write(ss)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool_index = pool_index
		self.sized_str_entry.pointers[0].data_offset = offset
		self.create_data_entry(self.sized_str_entry, (buffer_0, buffer_1))

	def collect(self):
		self.assign_ss_entry()

	def load(self, file_path):
		ss, buffer_0, buffer_1 = self._get_data(file_path)
		self.sized_str_entry.data_entry.update_data((buffer_0, buffer_1))
		self.sized_str_entry.pointers[0].update_data(ss, update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		try:
			buff = self.sized_str_entry.data_entry.buffer_datas[1]
		except:
			print("Found no buffer data for", name)
			return
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(buff)
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for an FDB"""
		buffer_0 = self.file_entry.basename.encode(encoding='utf8')
		buffer_1 = self.get_content(file_path)
		ss = struct.pack("I28s", len(buffer_1), b'')
		return ss, buffer_0, buffer_1

	def open_command(self, f):
		command_path = os.path.join(os.getcwd(), "sql_commands", f+".sql")
		print(command_path, os.path.isfile(command_path))
		with open(command_path, "r") as file:
			return file.read()

	def rename_content(self, name_tuples):
		command = None
		if is_pz(self.ovl) or is_pz16(self.ovl):
			if "zoopedia" in self.file_entry.name:
				command = self.open_command("pz_zoopedia")
		if command:

			logging.info(f"Executing command '' on {self.file_entry.name}")
			try:
				temp_dir, out_dir_func = self.get_tmp_dir()
				fdb_path = self.extract(out_dir_func, False, None)[0]
				con = sqlite3.connect(fdb_path)
				cur = con.cursor()

				for old, new in name_tuples:
					command_replaced = command.replace("ORIGINAL", old).replace("NEW", new)
					# print(command_replaced)
					cur.executescript(command_replaced)
				# Save (commit) the changes
				con.commit()
				con.close()
				self.load(fdb_path)
				shutil.rmtree(temp_dir)
			except BaseException as err:
				print(err)

