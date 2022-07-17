from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UbyteEnum


class MeshFormat(UbyteEnum):
	Separate = 0
	Interleaved32 = 1
	Interleaved48 = 2
