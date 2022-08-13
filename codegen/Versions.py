from codegen.naming_conventions import name_enum_key
from codegen.expression import Version


base_ver_attrs = ("id", "supported", "custom", "ext")

class Versions:
	"""Creates and writes a version block"""

	@staticmethod
	def format_id(version_id):
		return version_id.lower()

	def __init__(self, parser):
		self.parent = parser
		self.versions = []

	def read(self, xml_struct):
		self.versions.append(xml_struct)

	def write(self, out_file):
		if self.versions:
			with open(out_file, "w", encoding=self.parent.encoding) as stream:
				stream.write(f"from enum import Enum\n\n\n")

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
							if " " in val:
								conds_list.append(f"context.{name} in ({', '.join([str(Version(nr)) for nr in val.split(' ')])})")
							else:
								conds_list.append(f"context.{name} == {str(Version(val))}")
					stream.write("\n\tif " + " and ".join(conds_list) + ":")
					stream.write("\n\t\treturn True")
					stream.write("\n\n\n")

					stream.write(f"def set_{self.format_id(version.attrib['id'])}(context):")
					for k, v in version.attrib.items():
						if k not in base_ver_attrs:
							suffix = ""
							if k in self.parent.verattrs:
								name, attr_type = self.parent.verattrs[k]
								if attr_type and self.parent.tag_dict[attr_type.lower()] == 'bitfields':
									suffix = "._value"
							else:
								name = k.lower()
							val = v.strip()
							if " " in val:
								val = val.split(" ")[0]
							stream.write(f"\n\tcontext.{name}{suffix} = {str(Version(val))}")
					stream.write("\n\n\n")

				# go through all the games, record them and map defaults to versions
				full_name_key_map = {}
				version_default_map = {}
				version_game_map = {}
				for version in self.versions:
					version_default_map[version.attrib['id']] = set()
					game_names = version.text.split(', ')
					for i, game_name in enumerate(game_names):
						game_name = game_name.strip()
						# detect defaults and add them to the map
						if len(game_name) > 4:
							if game_name[:2] == '{{' and game_name[-2:] == '}}':
								game_name = game_name[2:-2]

								version_default_map[version.attrib['id']].add(name_enum_key(game_name))
								game_names[i] = game_name
						if game_name not in full_name_key_map:
							full_name_key_map[game_name] = name_enum_key(game_name)
					version_game_map[version.attrib['id']] = [full_name_key_map[game_name] for game_name in game_names]

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

