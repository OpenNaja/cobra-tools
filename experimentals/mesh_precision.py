import math

from generated.formats.ms2.compounds.ChunkedMesh import ChunkedMesh
from generated.formats.ms2.compounds.packing_utils import PACKEDVEC_MAX

precisions = [(8.0, 7.629452738910913e-06), (512.0, 0.0004885197849944234), (1024.0, 0.0009775171056389809), (2048.0, 0.001956947147846222), (4096.0, 0.003921568859368563)]

for base, prec in precisions:

	print(f"original: {base}, {prec}")
	print(f"restored: {base}, {ChunkedMesh.get_precision(base)}")
	print(f"newresto: {base}, {(base + (base*base / PACKEDVEC_MAX)) / PACKEDVEC_MAX}")
	base_exp = math.log2(base)
	error = 4 ** (base_exp - 10.0)
	new = (error + base) / PACKEDVEC_MAX
	print(f"error: {error}")
