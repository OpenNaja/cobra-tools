
class Versions:
	"""Creates and writes a version block"""

	def __init__(self, parser):
		self.parent = parser
		self.versions = []

	def read(self, xml_struct):
		self.versions.append(xml_struct)

	def write(self, out_file):
		full_game_names = []
		if self.versions:
			with open(out_file, "w") as stream:
				for version in self.versions:
					stream.write(f"def is_{version.attrib['id'].lower()}(inst):")
					conds_list = []
					for k, v in version.attrib.items():
						if k != "id":
							name = k.lower()
							val = v.strip()
							if " " in val:
								conds_list.append(f"inst.{name} in ({val.replace(' ', ', ')})")
							else:
								conds_list.append(f"inst.{name} == {val}")
					stream.write("\n\tif " + " and ".join(conds_list) + ":")
					stream.write("\n\t\treturn True")
					stream.write("\n\n\n")

					stream.write(f"def set_{version.attrib['id'].lower()}(inst):")
					for k, v in version.attrib.items():
						if k != "id":
							name = k.lower()
							val = v.strip()
							if " " in val:
								val = val.split(" ")[0]
							stream.write(f"\n\tinst.{name} = {val}")
					stream.write("\n\n\n")

				# write game lookup function
				stream.write(f"def get_game(inst):")
				for version in self.versions:
					stream.write(f"\n\tif is_{version.attrib['id'].lower()}(inst):")
					full_game_name = version.text.replace('"', '').strip()
					full_game_names.append(full_game_name)
					stream.write(f"\n\t\treturn '{full_game_name}'")
				stream.write("\n\treturn 'Unknown Game'")
				stream.write("\n\n\n")

				full_game_names.sort()
				full_game_names.append("Unknown Game")
				# write game list
				stream.write(f"games = {str(full_game_names)}")
				stream.write("\n\n\n")
