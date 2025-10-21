import os
from typing import TYPE_CHECKING, TextIO
if TYPE_CHECKING:
    from . import Config, Element
    from .XmlParser import XmlParser

from .expression import Version
from .naming_conventions import name_enum_key
from .path_utils import module_path_to_import_path, to_import_path

base_ver_attrs = ("id", "supported", "custom", "ext")


def split_parenthesis_aware(input_string: str, delimiter: str) -> list[str]:
	split_string: list[str] = []
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
	def get_default_games(version: 'Element') -> tuple[list[str], list[str]]:
		game_names = split_parenthesis_aware(version.text, delimiter=', ')
		default_games: list[str] = []
		all_games: list[str] = []
		for name in game_names:
			if name[:2] == "{{" and name[-2:] == "}}":
				name = name[2:-2]
				default_games.append(name)
			all_games.append(name)
		return default_games, all_games

	@staticmethod
	def format_id(version_id: str) -> str:
		return version_id.lower()

	def __init__(self, parser: 'XmlParser', gen_dir: str) -> None:
		self.parent: XmlParser = parser
		self.gen_dir: str = gen_dir
		self.versions: list['Element'] = []

	def read(self, xml_struct: 'Element') -> None:
		# apply Version(num) for every entry in a version-defining attribute
		# can't do this in xmlparser apply_conventions because it doesn't know
		# which attributes are the version-defining ones
		for k, v in tuple(xml_struct.attrib.items()):
			if k not in base_ver_attrs:
				# it must be a version-denoting attribute
				values = v.split()
				xml_struct.attrib[k] = ', '.join([str(Version(value)) for value in values])
		self.versions.append(xml_struct)

	def write(self, out_file: str) -> None:
		if os.path.exists(out_file):
			with open(out_file, "r", encoding=self.parent.encoding) as f:
				content = f.read()
				# If generated function is present, assume the file is complete and skip
				if "def get_game(context):" in content:
					return
		if self.versions:
			with open(out_file, "a", encoding=self.parent.encoding) as stream:
				stream.write(f"from enum import Enum\n\n")
				stream.write(f"from {to_import_path(self.gen_dir)}.base_version import VersionBase\n")
				if self.parent.verattrs:
					for verattr_name, (verattr_access, verattr_type) in self.parent.verattrs.items():
						if verattr_type is not None:
							import_path = module_path_to_import_path(self.parent.path_dict[verattr_type], self.gen_dir)
							stream.write(f"from {import_path} import {verattr_type}\n")
				stream.write(f"\n\n")

				# override any inherited versions by replacing
				versions_decimated = {}
				for version in self.versions:
					versions_decimated[version.attrib['id']] = version
				self.versions[:] = sorted(versions_decimated.values(), key=lambda v: v.attrib['id'])

				for version in self.versions:
					self.write_is_version(stream, version)
					self.write_set_version(stream, version)

				# go through all the games, record them and map defaults to versions
				full_name_key_map: dict[str, str] = {}
				version_default_map: dict[str, set[str]] = {}
				version_game_map: dict[str, list[str]] = {}
				for version in self.versions:
					version_default_map[version.attrib['id']] = set()
					default_games, all_games = self.get_default_games(version)
					for game in default_games:
						version_default_map[version.attrib['id']].add(name_enum_key(game))
					for game in all_games:
						if game not in full_name_key_map:
							full_name_key_map[game] = name_enum_key(game)
					version_game_map[version.attrib['id']] = [full_name_key_map[game_name] for game_name in all_games]

				self.write_games_enum(full_name_key_map, stream)

				self.write_get_game(stream, version_game_map)

				self.write_set_game(stream, version_default_map, version_game_map)

				if self.parent.verattrs:
					# generating version objects to store the extra attributes like ext, supported and games.

					# generate a base version class for this file format
					version_class = f'{self.parent.format_name.capitalize()}Version'
					self.write_version_class(stream, version_class)

					# generate a specific object for every version ID
					for version in self.versions:
						self.write_version_obj(stream, version, version_class)

					stream.write(f"\navailable_versions = [{', '.join([self.format_id(version.attrib['id']) for version in self.versions])}]")
					stream.write("\n")

	def write_version_class(self, stream: TextIO, version_class: str) -> None:
		stream.write(f"class {version_class}(VersionBase):\n\n")
		stream.write(f"\t_file_format = {repr(self.parent.format_name.lower())}\n")
		stream.write(f"\t_verattrs = ({', '.join(repr(attr) for attr in self.parent.verattrs)})\n\n")
		verattr_arguments = ', '.join([f'{verattr}=()' for verattr in self.parent.verattrs])
		stream.write(f"\tdef __init__(self, *args, {verattr_arguments}, **kwargs):\n")
		stream.write(f'\t\tsuper().__init__(*args, **kwargs)\n')
		for verattr in self.parent.verattrs:
			stream.write(f'\t\tself.{verattr} = self._force_tuple({verattr})\n')
		stream.write("\n\n")

	def write_version_obj(self, stream: TextIO, version: 'Element', version_class: str) -> None:
		stream.write(f"{self.format_id(version.attrib['id'])} = {version_class}(")
		stream.write(f"id={repr(version.attrib['id'])}")
		for verattr, (access, attr_type) in self.parent.verattrs.items():
			values: str | None = version.attrib.get(verattr)
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
			stream.write(f", ext=({', '.join([repr(extension) for extension in version.attrib['ext'].split()])},)")
		default_games, all_games = self.get_default_games(version)
		stream.write(f", primary_games=[{', '.join([f'games.{name_enum_key(game)}' for game in default_games])}]")
		stream.write(f", all_games=[{', '.join([f'games.{name_enum_key(game)}' for game in all_games])}]")
		stream.write(")\n")

	def write_games_enum(self, full_name_key_map, stream: TextIO) -> None:
		# define game enum
		enum_keys = [(key, full_name) for full_name, key in full_name_key_map.items()]
		enum_keys.sort()
		enum_keys.append(("UNKNOWN", "Unknown Game"))
		stream.write(
			f"games = Enum('Games', {enum_keys})")
		stream.write("\n\n\n")

	def write_set_version(self, stream: TextIO, version: 'Element') -> None:
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

	def write_is_version(self, stream: TextIO, version: 'Element') -> None:
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

	def write_get_game(self, stream: TextIO, version_game_map) -> None:
		# write game lookup function
		stream.write(f"def get_game(context):")
		stream.write(f"\n\tversions = []")
		for version in self.versions:
			version_id = version.attrib['id']
			stream.write(f"\n\tif is_{self.format_id(version_id)}(context):")
			stream.write(
				f"\n\t\tversions.extend([{', '.join([f'games.{key}' for key in version_game_map[version_id]])}])")
		stream.write(f"\n\tif not versions:")
		stream.write("\n\t\tversions.extend([games.UNKNOWN])")
		stream.write("\n\treturn versions")
		stream.write("\n\n\n")

	def write_set_game(self, stream: TextIO, version_default_map, version_game_map) -> None:
		# write game version setting function
		stream.write(f"def set_game(context, game):")
		stream.write(f"\n\tif isinstance(game, str):")
		stream.write(f"\n\t\tif game in games._member_names_:")
		stream.write(f"\n\t\t\tgame = games[game]")
		stream.write(f"\n\t\telse:")
		stream.write(f"\n\t\t\tgame = games(game)")
		# first check all the defaults
		for version in self.versions:
			if len(version_default_map[version.attrib['id']]) > 0:
				stream.write(
					f"\n\tif game in {{{', '.join([f'games.{key}' for key in version_default_map[version.attrib['id']]])}}}:")
				stream.write(f"\n\t\treturn set_{self.format_id(version.attrib['id'])}(context)")
		# then the rest
		for version in self.versions:
			non_default_games = set(version_game_map[version.attrib['id']]) - version_default_map[version.attrib['id']]
			if len(non_default_games) > 0:
				stream.write(f"\n\tif game in {{{', '.join([f'games.{key}' for key in non_default_games])}}}:")
				stream.write(f"\n\t\treturn set_{self.format_id(version.attrib['id'])}(context)")
		stream.write("\n\n\n")
