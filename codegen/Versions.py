
class Versions:
	"""Creates and writes a version block"""

	def __init__(self, parser):
		self.parent = parser
		self.versions = []

	def read(self, xml_struct):
		self.versions.append(xml_struct)

	def write(self, out_file):
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
