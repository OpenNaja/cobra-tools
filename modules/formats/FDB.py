from __future__ import annotations
import logging
import os
import shutil
import sqlite3
import struct
import re
from collections import namedtuple

from generated.formats.ovl_base.versions import is_pz, is_pz16
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import djb2


class FdbLoader(BaseFile):
	extension = ".fdb"

	def create(self, file_path):
		root_data, buffer_0, buffer_1 = self._get_data(file_path)
		self.write_root_bytes(root_data)
		self.create_data_entry((buffer_0, buffer_1))
		# patch these
		self.data_entry.size_1 = self.data_entry.size_2
		self.data_entry.size_2 = 0

	def extract(self, out_dir):
		name = self.name
		buff = self.data_entry.buffer_datas[1]
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(buff)
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for an FDB"""
		buffer_0 = self.basename.encode(encoding='utf8')
		buffer_1 = self.get_content(file_path)
		root_entry = struct.pack("I28s", len(buffer_1), b'')
		return root_entry, buffer_0, buffer_1

	@staticmethod
	def open_command(f):
		pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
		command_path = os.path.join(pkg_dir, "sql_commands", f"{f}.sql")
		with open(command_path, "r") as file:
			return file.read()

	ScriptContext = namedtuple('ScriptContext', ['name', 'command', 'num_strings', 'find_strings'])

	def context_is_valid(self, context: ScriptContext, name_tuples):
		if not context or not name_tuples:
			return False
		# Require at least N tuples from the GUI, strings over context.num_strings are ignored
		if len(name_tuples) < context.num_strings:
			logging.warning(f"Required replacement strings missing for {self.name}")
			logging.info(
				f"Skipping {self.name}. Script strings in need of replacement: {context.find_strings}")
			logging.info(
				f"Rename Contents on this FDB needs {context.num_strings} strings in both Find/Replace separated by new lines.")
			return False
		return context.name and context.command and context.find_strings

	def are_strs_in_fdb(self, fdb_path: str, context: ScriptContext, name_tuples):
		not_found = []
		with open(fdb_path, 'rb', 0) as file:
			for tup in name_tuples[:context.num_strings]:
				find = tup[0]
				if find.encode() in file.read():
					return True
				not_found.append(find)
		logging.error(f'SQL error: {not_found} not found in {self.name}. Aborting SQL commands.')
		return False

	def get_script_context(self):
		# The SQL strings per script
		script_strings = {
			"animals": [("ORIGINAL_SPECIES", "NEW_SPECIES")],
			"education": [("ORIGINAL_SPECIES", "NEW_SPECIES")],
			"research": [("ORIGINAL_SPECIES", "NEW_SPECIES")],
			"zoopedia": [("ORIGINAL_SPECIES", "NEW_SPECIES")]
		}
		if is_pz(self.ovl) or is_pz16(self.ovl):
			for s in script_strings.keys():
				if s in self.name:
					# The SQL strings for the current context
					find_strings = list(script_strings.get(s, [()]))
					return self.ScriptContext(s, self.open_command(f"pz_{s}"), len(find_strings), find_strings)

	@staticmethod
	def fix_animal_definition(cur, pattern, new_species: str, column: str, default_suffix: str):
		cur.execute(f"SELECT {column} FROM AnimalDefinitions;")
		prefab_col = cur.fetchone()
		if prefab_col:
			prefab_col_search = pattern.search(prefab_col[0])
			suffix = prefab_col_search.group(0) if prefab_col_search else default_suffix
			
			logging.info(f"Setting AnimalDefinitions {column} to '{new_species + suffix}' for '{new_species}'")
			cur.execute(f"UPDATE AnimalDefinitions SET {column} = '{new_species + suffix}' WHERE AnimalType LIKE '{new_species}';")

	def rename_content(self, name_tuples):
		# The current script context e.g. "animals" or "research"
		context = self.get_script_context()

		if self.context_is_valid(context, name_tuples):
			logging.info(f"Executing command '{context.name}' on {self.name}")
			try:
				with self.get_tmp_dir_func() as out_dir_func:
					fdb_path = self.extract(out_dir_func)[0]

					# Clean up with VACUUM first
					try:
						con = sqlite3.connect(fdb_path)
						con.execute("VACUUM")
					except sqlite3.Error:
						logging.exception(f"SQL error query failed")
					finally:
						con.close()

					# Before running SQL commands, verify the strings exist or you will get empty FDBs
					if self.are_strs_in_fdb(fdb_path, context, name_tuples):
						con = sqlite3.connect(fdb_path)
						cur = con.cursor()
						try:
							command_replaced = context.command
							for i, find in enumerate(context.find_strings):
								command_replaced = command_replaced.replace(
									find[0], name_tuples[i][0]).replace(find[1], name_tuples[i][1])

							# Calculate new research hash
							# CALCULATED_HASH gets added to the original ResearchID in the SQL script
							# Uses both Find and Replace strings for reduced chance of collisions
							if context.name == "research":
								command_replaced = command_replaced.replace("CALCULATED_HASH", str(djb2(
									name_tuples[0][0] + name_tuples[0][1])))

							cur.executescript(command_replaced)

							# Fix AnimalDefinitions
							if context.name == "animals":
								new_species = name_tuples[0][1]
								re_game = re.compile(r"((_Male|_Female|_Juvenile)?_Game)", re.IGNORECASE)
								re_visual = re.compile(r"(_(Male|Female|Juvenile)_Visuals)", re.IGNORECASE)
								self.fix_animal_definition(cur, re_game, new_species, "AdultMaleGamePrefab", "_Game")
								self.fix_animal_definition(cur, re_visual, new_species, "AdultMaleVisualPrefab", "_Male_Visuals")
								self.fix_animal_definition(cur, re_game, new_species, "AdultFemaleGamePrefab", "_Game")
								self.fix_animal_definition(cur, re_visual, new_species, "AdultFemaleVisualPrefab", "_Female_Visuals")
								self.fix_animal_definition(cur, re_game, new_species, "JuvenileGamePrefab", "_Game")
								self.fix_animal_definition(cur, re_visual, new_species, "JuvenileVisualPrefab", "_Juvenile_Visuals")

							# Save (commit) the changes
							con.commit()
						except sqlite3.Error as e:
							logging.error(f"SQL error: {str(e)}")
						finally:
							con.close()

					self.remove()
					loader = self.ovl.create_file(fdb_path, self.name)
					self.ovl.register_loader(loader)
			except:
				logging.exception(f"FDB command failed")
		elif context:
			logging.error(f"SQL Script context '{context.name}' invalid on {self.name}")


