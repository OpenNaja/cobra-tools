import os

import bpy
import mathutils

from generated.formats.ms2.compounds.packing_utils import pack_swizzle
from generated.formats.spl.compounds.SplRoot import SplRoot
from generated.formats.spl.compounds.SplData import SplData


def pack(c_v, b_v, s):
	c_v.x, c_v.y, c_v.z = pack_swizzle([i / s for i in b_v])


def save(filepath=""):
	# get selected curve b_ob
	b_ob = bpy.context.object
	b_cu = b_ob.data
	if b_ob.type != "CURVE":
		raise AttributeError(f"Can only export curve objects")
	context = object()
	# export the curve data
	spl_root = SplRoot(context)
	spline_data = SplData(context)
	spl_root.spline_data.data = spline_data

	# get basic data from b_spline
	b_spline = b_cu.splines[0]
	spl_root.count = len(b_spline.bezier_points)
	spl_root.length = b_spline.calc_length()

	pack(spline_data.offset, b_ob.location, 1.0)

	# for key, bezier in zip(spline_data.keys, b_spline.bezier_points):
	#     bezier.co = unpack(key.pos, spline_data.scale)
	#     bezier.handle_left = bezier.co + unpack(key.handle_left, key.handle_scale)
	#     bezier.handle_right = bezier.co + unpack(key.handle_right, key.handle_scale)

	SplRoot.to_xml_file(spl_root, filepath)
	return f"Finished SPL export",
