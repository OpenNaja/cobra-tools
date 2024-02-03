import bpy
from collections import defaultdict

# adapted from
# https://blender.stackexchange.com/questions/157828/how-to-duplicate-a-certain-collection-using-python


def copy_objects(from_col, to_col, linked, dupe_lut, replacer, mat_lut):
	for o in from_col.objects:
		dupe = o.copy()
		dupe.name = replacer(o.name)
		if not linked and o.data:
			dupe.data = dupe.data.copy()
			dupe.data.name = replacer(dupe.data.name)
			# use LUT for mats to only duplicate once per run
			if dupe.type == "MESH" and mat_lut is not None:
				for i, mat in enumerate(dupe.data.materials):
					# fallback copy_name if replacer changes nothing
					new_name = replacer(mat.name)
					if new_name != mat.name:
						name_key = new_name
					else:
						name_key = f"{mat.name}_copy"
					# find or store previously copied material
					if name_key in mat_lut:
						copy_mat = mat_lut[name_key]
					else:
						copy_mat = mat.copy()
						copy_mat.name = name_key
						mat_lut[name_key] = copy_mat
					# update slot
					dupe.data.materials[i] = copy_mat
		to_col.objects.link(dupe)
		dupe_lut[o] = dupe


def copy(parent, collection, linked=False, replacer=None, share_materials=True):
	assert parent != collection
	dupe_lut = defaultdict(lambda: None)
	mat_lut = None if share_materials else {}

	def _copy(parent, collection, linked=False):
		cc = bpy.data.collections.new(replacer(collection.name))
		copy_objects(collection, cc, linked, dupe_lut, replacer, mat_lut)

		for c in collection.children:
			_copy(cc, c, linked)

		parent.children.link(cc)

	_copy(parent, collection, linked)
	# print(dupe_lut)
	for o, dupe in tuple(dupe_lut.items()):
		parent = dupe_lut[o.parent]
		if parent:
			dupe.parent = parent
