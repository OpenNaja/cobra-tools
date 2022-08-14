from generated.formats.matcol.basic import basic_map
from generated.formats.matcol.compounds.MaterialcollectionInfoHeader import MaterialcollectionInfoHeader
from generated.formats.ovl_base import OvlContext
from generated.io import IoFile


class MatcolFile(MaterialcollectionInfoHeader, IoFile):

	basic_map = basic_map

	def __init__(self):
		super().__init__(OvlContext())

	def load(self, filepath, commands=(), mute=False):
		eof = super().load(filepath)
		for layer in self.layers:
			for info, name in zip(layer.infos, layer.info_names):
				info.name = name
			for att, name in zip(layer.attribs, layer.attrib_names):
				att.name = name


if __name__ == "__main__":
	m = MatcolFile()
	m.load("C:/Users/arnfi/Desktop/carch/carcharodontosaurus.matcol")
	print(m)
