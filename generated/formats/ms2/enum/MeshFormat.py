from generated.formats.base.basic import fmt_member
from generated.formats.base.enum import UbyteEnum


class MeshFormat(UbyteEnum):
	SEPARATE = 0
	INTERLEAVED_32 = 1
	INTERLEAVED_48 = 2
