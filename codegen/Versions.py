from codegen.expression import Version
from codegen.Imports import Imports
from codegen.naming_conventions import name_enum_key

base_ver_attrs = ("id", "supported", "custom", "ext")

def split_parenthesis_aware(input_string, delimiter):
	split_string = []
	par_level = 0
	last_start = 0
	i = 0
	while i < len(input_string):
		char = input_string[i]
		if char == "(":
			par_level += 1
		elif char == ")":
			par_level -= 1
		else:
			if not par_level:
				if input_string[i:i + len(delimiter)] == delimiter:
					split_string.append(input_string[last_start:i])
					i += len(delimiter)
					last_start = i
					continue
		i += 1
	# there is a part left
	split_string.append(input_string[last_start:i])
	return split_string


class Versions:
	"""Creates and writes a version block"""

	@staticmethod
	def get_default_games(version):
		game_names = split_parenthesis_aware(version.text, delimiter=', ')
		default_games = []
		all_games = []
		for name in game_names:
			if name[:2] == "{{" and name[-2:] == "}}":
				name = name[2:-2]
				default_games.append(name)
			all_games.append(name)
		return default_games, all_games

	@staticmethod
	def format_id(version_id):
		return version_id.lower()

	def __init__(self, parser):
		self.parent = parser
		self.versions = []

	def read(self, xml_struct):
		# apply Version(num) for every entry in a version-defining attribute
		# can't do this in xmlparser apply_conventions because it doesn't know
		# which attributes are the version-defining ones
		for k, v in tuple(xml_struct.attrib.items()):
			if k not in base_ver_attrs:
				# it must be a version-denoting attribute
				values = v.split()
				xml_struct.attrib[k] = ', '.join([str(Version(value)) for value in values])
		self.versions.append(xml_struct)

	def write(self, out_file):
		if self.versions:
			with open(out_file, "a", encoding=self.parent.encoding) as stream:
				stream.write(f"from enum import Enum\n\n")
				stream.write(f"from generated.base_version import VersionBase\n")
				if self.parent.verattrs:
					for verattr_name, (verattr_access, verattr_type) in self.parent.verattrs.items():
						if verattr_type is not None:
							import_path = Imports.import_from_module_path(self.parent.path_dict[verattr_type])
							stream.write(f"from {import_path} import {verattr_type}\n")
				stream.write(f"\n\n")

				for version in self.versions:
					stream.write(f"def is_{self.format_id(version.attrib['id'])}(context):")
					conds_list = []
					for k, v in version.attrib.items():
						if k not in base_ver_attrs:
							if k in self.parent.verattrs:
								name = self.parent.verattrs[k][0]
							else:
								name = k.lower()
							val = v.strip()
							if ", " in val:
								conds_list.append(f"context.{name} in ({val})")
							else:
								conds_list.append(f"context.{name} == {val}")
					stream.write("\n\tif " + " and ".join(conds_list) + ":")
					stream.write("\n\t\treturn True")
					stream.write("\n\n\n")

					stream.write(f"def set_{self.format_id(version.attrib['id'])}(context):")
					for k, v in version.attrib.items():
						if k not in base_ver_attrs:
							suffix = ""
							if k in self.parent.verattrs:
								name, attr_type = self.parent.verattrs[k]
								if attr_type and self.parent.tag_dict[attr_type.lower()] in self.parent.bitstruct_types:
									suffix = "._value"
							else:
								name = k.lower()
							val = v.strip()
							if ", " in val:
								val = val.split(", ")[0]
							stream.write(f"\n\tcontext.{name}{suffix} = {val}")
					stream.write("\n\n\n")

				# go through all the games, record them and map defaults to versions
				full_name_key_map = {}
				version_default_map = {}
				version_game_map = {}
				for version in self.versions:
					version_default_map[version.attrib['id']] = set()
					default_games, all_games = self.get_default_games(version)
					for game in default_games:
						version_default_map[version.attrib['id']].add(name_enum_key(game))
					for game in all_games:
						if game not in full_name_key_map:
							full_name_key_map[game] = name_enum_key(game)
					version_game_map[version.attrib['id']] = [full_name_key_map[game_name] for game_name in all_games]

				# define game enum
				full_name_key_map = {full_name: key for full_name, key in sorted(full_name_key_map.items(), key=lambda item: item[1])}
				full_name_key_map["Unknown Game"] = "UNKNOWN_GAME"
				stream.write(f"games = Enum('Games',{repr([(key, full_name) for full_name, key in full_name_key_map.items()])})")
				stream.write("\n\n\n")

				# write game lookup function
				stream.write(f"def get_game(context):")
				for version in self.versions:
					stream.write(f"\n\tif is_{self.format_id(version.attrib['id'])}(context):")
					stream.write(f"\n\t\treturn [{', '.join([f'games.{key}' for key in version_game_map[version.attrib['id']]])}]")
				stream.write("\n\treturn [games.UNKOWN_GAME]")
				stream.write("\n\n\n")

				# write game version setting function
				stream.write(f"def set_game(context, game):")
				stream.write(f"\n\tif isinstance(game, str):")
				stream.write(f"\n\t\tgame = games(game)")
				# first check all the defaults
				for version in self.versions:
					if len(version_default_map[version.attrib['id']]) > 0:
						stream.write(f"\n\tif game in {{{', '.join([f'games.{key}' for key in version_default_map[version.attrib['id']]])}}}:")
						stream.write(f"\n\t\treturn set_{self.format_id(version.attrib['id'])}(context)")
				# then the rest
				for version in self.versions:
					non_default_games = set(version_game_map[version.attrib['id']]) - version_default_map[version.attrib['id']]
					if len(non_default_games) > 0:
						stream.write(f"\n\tif game in {{{', '.join([f'games.{key}' for key in non_default_games])}}}:")
						stream.write(f"\n\t\treturn set_{self.format_id(version.attrib['id'])}(context)")
				stream.write("\n\n\n")

				if self.parent.verattrs:
					version_class = f'{self.parent.format_name.capitalize()}Version'
					stream.write(f"class {version_class}(VersionBase):\n\n")
					stream.write(f"\t_file_format = {repr(self.parent.format_name.lower())}\n")
					stream.write(f"\t_verattrs = ({', '.join(repr(attr) for attr in self.parent.verattrs)})\n\n")
					verattr_arguments = ', '.join([f'{verattr}=()'for verattr in self.parent.verattrs])
					stream.write(f"\tdef __init__(self, *args, {verattr_arguments}, **kwargs):\n")
					stream.write(f'\t\tsuper().__init__(*args, **kwargs)\n')
					for verattr in self.parent.verattrs:
						stream.write(f'\t\tself.{verattr} = self._force_tuple({verattr})\n')
					stream.write("\n\n")

					for version in self.versions:
						default_games, all_games = self.get_default_games(version)
						stream.write(f"{self.format_id(version.attrib['id'])} = {version_class}(")
						stream.write(f"id={repr(version.attrib['id'])}")
						for verattr, (access, attr_type) in self.parent.verattrs.items():
							values = version.attrib.get(verattr)
							if values:
								values = values.split(', ')
								str_values = []
								for value in values:
									if attr_type:
										str_values.append(f'{attr_type}.from_value({value})')
									else:
										str_values.append(value)
								stream.write(f", {verattr}=({', '.join(str_values)},)")
						if version.attrib.get("supported"):
							stream.write(f", supported={version.attrib['supported']}")
						if version.attrib.get("custom"):
							stream.write(f", custom={version.attrib['custom']}")
						if version.attrib.get("ext"):
							stream.write(f", ext=({', '.join([repr(extension) for extension in version.attrib['ext'].split()],)})")
						default_games, all_games = self.get_default_games(version)
						default_games = [f'games.{name_enum_key(game)}' for game in default_games]
						all_games = [f'games.{name_enum_key(game)}' for game in all_games]
						stream.write(f", primary_games=[{', '.join(default_games)}]")
						stream.write(f", all_games=[{', '.join(all_games)}]")
						stream.write(")\n")

					stream.write(f"\nversions = [{', '.join([self.format_id(version.attrib['id']) for version in self.versions])}]")
					stream.write("\n")