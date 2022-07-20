from source.formats.base.basic import fmt_member
from generated.formats.dds.enum import UintEnum


class FourCC(UintEnum):

	"""
	An unsigned 32-bit integer, describing the compression type.
	Four-character codes for specifying compressed or custom formats. Possible values include: DXT1, DXT2, DXT3, DXT4, or DXT5.
	A FourCC of DX10 indicates the prescense of the DDS_HEADER_DXT10 extended header, and the dxgiFormat member of that structure
	indicates the true format. When using a four-character code, dwFlags must include DDPF_FOURCC.
	"""
	LINEAR = 0x00000000
	DXT_1 = 0x31545844
	DXT_2 = 0x32545844
	DXT_3 = 0x33545844
	DXT_4 = 0x34545844
	DXT_5 = 0x35545844
	RXGB = 0x42475852
	ATI_1 = 0x31495441
	ATI_2 = 0x32495441
	DX_10 = 0x30315844
