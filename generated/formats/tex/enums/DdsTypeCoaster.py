from generated.base_enum import BaseEnum
from generated.formats.base.basic import Ubyte


class DdsTypeCoaster(BaseEnum):

	"""
	maps the OVL's dds type to name of compression format
	PC1 uses [1, 48, 59, 74, 76, 97, 98, 101, 102, 105, 121, 123, 127]
	"""

	__name__ = 'DdsTypeCoaster'
	_storage = Ubyte


	# used in PC1
	UNK0 = 1

	# used in PC1
	UNK1 = 48

	# used in PC1
	UNK2 = 59

	# used in PC1, ZTUAC ele heights textures
	D24_UNORM_S8_UINT = 74

	# used in PC1
	D24_UNORM_S8_UINT_B = 76

	# used a lot in PC1
	BC1_UNORM = 97

	# used a lot in PC1
	BC1_UNORM_SRGB = 98

	# not used in PC1
	BC2_UNORM = 99

	# not used in PC1
	BC2_UNORM_SRGB = 100

	# in PC1, exclusively used on icons
	BC3_UNORM_SRGB = 101

	# used rarely in PC1, and apparently on very bright textures where SRGB does not matter
	# 'Content0\\Environment\\Scenery\\Themes\\PC_PlanetCoaster\\PC_Signs\\PC_Signs_Park',
	# 'Content0\\Environment\\Scenery\\Themes\\FT_FairyTale\\FT_WallLamps',
	# 'Content0\\Environment\\Scenery\\Themes\\WS_Western\\WS_WallLamps',
	# 'Content0\\Environment\\Terrain\\TerrainEditor',
	# 'PDLC_GHB\\Environment\\Scenery\\ProtonBeam',
	# 'Content0\\Environment\\Scenery\\Themes\\WS_Western\\WS_Decorations',
	# 'Content0\\Environment\\Scenery\\Themes\\FT_FairyTale\\FT_IronChandelier'
	BC3_UNORM = 102

	# not used in PC1
	BC4_UNORM = 103

	# not used in PC1
	BC4_SNORM = 104

	# used in PC1
	BC5_UNORM = 105

	# not used in PC1
	BC5_SNORM = 106

	# used in PC1
	BC4_UNORM_B = 121

	# used in PC1
	UNK3 = 123

	# not used in PC1
	BC7_UNORM = 126

	# used in PC1
	BC7_UNORM_SRGB = 127
