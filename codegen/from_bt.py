import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from xml.dom import minidom


def read_bt(fp):
	root = ET.Element("root")
	is_open = False
	with open(fp, "r") as file:
		for line in file.readlines():
			if is_open:
				if line.startswith("} "):
					struct_name = line.split(" ")[1]
					print(struct_name)
					doc.tag = struct_name
					is_open = False
				else:
					# might be a field
					# print("field")
					if ";" in line:
						line = line.strip()
						if "//" in line:
							line, c = line.split("//")
						else:
							c = ""
						if not " " in line:
							continue
						if "Assert" in line:
							continue
						f = line.split(";")[0].strip()
						# print(f.split())
						dtype, tag = f.split()[:2]
						if "[" in tag:
							tag, arr1 = tag.split("[")
							arr1 = arr1.split("]")[0]
						else:
							arr1 = None
						if "(" in dtype:
							continue
						print(tag, dtype, c)
						field = ET.SubElement(doc, "field", name=tag, type=dtype)
						field.text = c.strip()
						if arr1:
							field.attrib["arr1"] = arr1
			else:
				if line.startswith("typedef struct {"):
					doc = ET.SubElement(root, "TEMP")
					is_open = True
					print("\nnew struct")

	xmlstr = minidom.parseString(ET.tostring(root, encoding='utf8', method='xml').decode()).toprettyxml(indent="   ")
	op = os.path.splitext(fp)[0]+".xml"
	with open(op, "w") as f:
		# f.write(ET.tostring(root, encoding='utf8', method='xml'))
		f.write(xmlstr)


if __name__ == "__main__":
	fp = "C:/Users/arnfi/Desktop/Ovl.bt"
	print(read_bt(fp))
