import bpy

from generated.formats.ms2.structs.packing_utils import pack_swizzle
from generated.formats.spl.structs.SplRoot import SplRoot
from generated.formats.spl.structs.SplData import SplData
from generated.formats.spl.structs.Key import Key


def pack(c_v, b_v, s):
	c_v.x, c_v.y, c_v.z = pack_swizzle([i / s for i in b_v])


def pack_int(c_v, b_v, s):
	c_v.x, c_v.y, c_v.z = pack_swizzle([int(round(i / s)) for i in b_v])


def get_max(list_of_b_vecs):
	return max(abs(c) for vec in list_of_b_vecs for c in vec)


def save(reporter, filepath=""):
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
	spline_data.scale = get_max([bezier.co for bezier in b_spline.bezier_points]) / 32767
	for bezier in b_spline.bezier_points:
		key = Key(context)
		spline_data.keys.append(key)
		pack_int(key.pos, bezier.co, spline_data.scale)
		left_rel = bezier.handle_left - bezier.co
		right_rel = bezier.handle_right - bezier.co
		key.handle_scale = get_max((left_rel, right_rel)) / 127
		pack_int(key.handle_left, left_rel, key.handle_scale)
		pack_int(key.handle_right, right_rel, key.handle_scale)

	with SplRoot.to_xml_file(spl_root, filepath) as xml_root:
		pass
	reporter.show_info(f"Exported {b_ob.name}")
