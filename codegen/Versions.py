from codegen.naming_conventions import name_enum_key
from codegen.expression import Version


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
		full_game_names = []
		if self.versions:
			with open(out_file, "w") as stream:
				stream.write(f"from enum import Enum\n\n\n")

				for version in self.versions:
					stream.write(f"def is_{self.format_id(version.attrib['id'])}(inst):")
					conds_list = []
					for k, v in version.attrib.items():
						if k != "id":
							name = k.lower()
							val = v.strip()
							if name == 'num':
								val = str(Version(val))
							if " " in val:
								conds_list.append(f"inst.{name} in ({val.replace(' ', ', ')})")
							else:
								conds_list.append(f"inst.{name} == {val}")
					stream.write("\n\tif " + " and ".join(conds_list) + ":")
					stream.write("\n\t\treturn True")
					stream.write("\n\n\n")

					stream.write(f"def set_{self.format_id(version.attrib['id'])}(inst):")
					for k, v in version.attrib.items():
						if k != "id":
							name = k.lower()
							val = v.strip()
							if " " in val:
								val = val.split(" ")[0]
							if name == "user_version":
								suffix = "._value"
							else:
								suffix = ""
								if name == "num":
									val = str(Version(val))
							stream.write(f"\n\tinst.{name}{suffix} = {val}")
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
				stream.write(f"def get_game(inst):")
				for version in self.versions:
					stream.write(f"\n\tif is_{self.format_id(version.attrib['id'])}(inst):")
					stream.write(f"\n\t\treturn [{', '.join([f'games.{key}' for key in version_game_map[version.attrib['id']]])}]")
				stream.write("\n\treturn [games.UNKOWN_GAME]")
				stream.write("\n\n\n")

				# write game version setting function
				stream.write(f"def set_game(inst, game):")
				# first check all the defaults
				for version in self.versions:
					if len(version_default_map[version.attrib['id']]) > 0:
						stream.write(f"\n\tif game in {{{', '.join([f'games.{key}' for key in version_default_map[version.attrib['id']]])}}}:")
						stream.write(f"\n\t\treturn set_{self.format_id(version.attrib['id'])}(inst)")
				# then the rest
				for version in self.versions:
					non_default_games = set(version_game_map[version.attrib['id']]) - version_default_map[version.attrib['id']]
					if len(non_default_games) > 0:
						stream.write(f"\n\tif game in {{{', '.join([f'games.{key}' for key in non_default_games])}}}:")
						stream.write(f"\n\t\treturn set_{self.format_id(version.attrib['id'])}(inst)")
				stream.write("\n\n\n")

