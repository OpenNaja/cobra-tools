from __future__ import annotations
import logging
import os
import shutil
import sqlite3
import struct
import traceback
import mmap
from collections import namedtuple

from generated.formats.ovl_base.versions import is_pz, is_pz16
from modules.formats.BaseFormat import BaseFile
from root_path import root_dir


class FdbLoader(BaseFile):
	extension = ".fdb"

	def create(self):
		root_entry, buffer_0, buffer_1 = self._get_data(self.file_entry.path)
		self.create_root_entry()
		self.write_data_to_pool(self.root_entry.struct_ptr, 2, root_entry)
		self.create_data_entry((buffer_0, buffer_1))

	def extract(self, out_dir):
		name = self.root_entry.name
		try:
			buff = self.data_entry.buffer_datas[1]
		except:
			raise AttributeError(f"Found no buffer data for {name}")
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(buff)
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for an FDB"""
		buffer_0 = self.file_entry.basename.encode(encoding='utf8')
		buffer_1 = self.get_content(file_path)
		root_entry = struct.pack("I28s", len(buffer_1), b'')
		return root_entry, buffer_0, buffer_1

	def open_command(self, f):
		command_path = os.path.join(root_dir, "sql_commands", f+".sql")
		with open(command_path, "r") as file:
			return file.read()

	@staticmethod
	def hash_djb2(s):
		hash = 5381
		for x in s:
			hash = (( hash << 5) + hash) + ord(x)
		return hash & 0xFFFFFFFF

	ScriptContext = namedtuple('ScriptContext', ['name', 'command', 'num_strings', 'find_strings'])
	def context_is_valid(self, context: ScriptContext, name_tuples):
		if not context or not name_tuples:
			return False
		# Require at least N tuples from the GUI, strings over context.num_strings are ignored
		if len(name_tuples) < context.num_strings:
			logging.warning(f"Required replacement strings missing for {self.file_entry.name}")
			logging.info(f"Skipping {self.file_entry.name}. Script strings in need of replacement: {context.find_strings}")
			logging.info(f"Rename Contents on this FDB needs {context.num_strings} strings in both Find/Replace separated by new lines.")
			return False
		return context.name and context.command and context.find_strings

	def rename_content(self, name_tuples):
		# The current script context e.g. "animals" or "research"
		context = None
		# The SQL strings per script
		script_strings = {
			"animals" : [("ORIGINAL_SPECIES", "NEW_SPECIES"), ("ORIGINAL_PREFAB", "NEW_PREFAB")],
			"education" : [("ORIGINAL_SPECIES", "NEW_SPECIES")],
			"research" : [("ORIGINAL_SPECIES", "NEW_SPECIES")],
			"zoopedia": [("ORIGINAL_SPECIES", "NEW_SPECIES")]
		}

		if is_pz(self.ovl) or is_pz16(self.ovl):
			for s in ("zoopedia", "research", "education", "animals"):
				if s in self.file_entry.name:
					# The SQL strings for the current context
					find_strings = list(script_strings.get(s, [()]))
					context = self.ScriptContext(s, self.open_command(f"pz_{s}"), len(find_strings), find_strings)
					break

		if self.context_is_valid(context, name_tuples):
			logging.info(f"Executing command '{s}' on {self.file_entry.name}")
			try:
				temp_dir, out_dir_func = self.get_tmp_dir()
				fdb_path = self.extract(out_dir_func)[0]

				# Clean up with VACUUM first
				try:
					con = sqlite3.connect(fdb_path)
					con.execute("VACUUM")
				except sqlite3.Error as e:
					logging.error(f"SQL error: {str(e)}")
				finally:
					con.close()

				# Before running SQL commands, verify the strings exist or you will get empty FDBs
				run = True
				with open(fdb_path, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
					for tup in name_tuples[:context.num_strings]:
						find = tup[0]
						if s.find(find.encode()) == -1:
							run = False
							logging.error(f'SQL error: "{find}" not found in {self.file_entry.name}. Aborting SQL commands.')
							break

				if run:
					con = sqlite3.connect(fdb_path)
					cur = con.cursor()
					try:
						command_replaced = context.command
						for i, find in enumerate(context.find_strings):
							command_replaced = command_replaced.replace(find[0], name_tuples[i][0]).replace(find[1], name_tuples[i][1])
						
						# Calculate new research hash
						# CALCULATED_HASH gets added to the original ResearchID in the SQL script
						# Uses both Find and Replace strings for reduced chance of collisions
						if context.name == "research":
							command_replaced = command_replaced.replace("CALCULATED_HASH", str(self.hash_djb2(name_tuples[0][0] + name_tuples[0][1])))

						cur.executescript(command_replaced)
						# Save (commit) the changes
						con.commit()
					except sqlite3.Error as e:
						logging.error(f"SQL error: {str(e)}")
						#logging.warning(f"Re-extracting {self.file_entry.name} due to failed SQL commands")
						# Possibly unncessary but safest
						#fdb_path = self.extract(out_dir_func, None)[0]
					finally:
						con.close()

				self.remove()
				self.ovl.create_file(fdb_path)
				shutil.rmtree(temp_dir)
			except BaseException as err:
				traceback.print_exc()
		elif context:
			logging.error(f'SQL Script context "{context.name}" invalid on {self.file_entry.name}')

