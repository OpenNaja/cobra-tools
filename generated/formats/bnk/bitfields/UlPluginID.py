from generated.bitfield import BasicBitfield
from generated.bitfield import BitfieldMember
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint


class UlPluginID(BasicBitfield):

	__name__ = 'ulPluginID'
	_storage = Uint
	plugin_id = BitfieldMember(pos=16, mask=0xffff0000, return_type=Int.from_value)
	company_id = BitfieldMember(pos=4, mask=0xfff0, return_type=Int.from_value)
	plugin_type = BitfieldMember(pos=0, mask=0xf, return_type=Int.from_value)

	def set_defaults(self):
		pass
