import bpy
from collections import defaultdict

# adapted from
# https://blender.stackexchange.com/questions/157828/how-to-duplicate-a-certain-collection-using-python


def copy_objects(from_col, to_col, linked, dupe_lut, replacer, share_materials):
	for ob in from_col.objects:
		dupe = ob.copy()
		dupe.name = replacer(ob.name)
		if not linked and ob.data:
			dupe.data = dupe.data.copy()
			dupe.data.name = replacer(ob.data.name)
			# use LUT for mats to only duplicate once per run
			if dupe.type == "MESH" and not share_materials:
				for i, mat in enumerate(dupe.data.materials):
					# find previously copied material
					if mat in dupe_lut:
						copy_mat = dupe_lut[mat]
					else:
						copy_mat = mat.copy()
						# fallback to name_copy if replacer changes nothing
						new_name = replacer(mat.name)
						if new_name != mat.name:
							copy_mat.name = new_name
						else:
							copy_mat.name = f"{mat.name}_copy"
						dupe_lut[mat] = copy_mat
					# update material slot
					dupe.data.materials[i] = copy_mat
		to_col.objects.link(dupe)
		dupe_lut[ob] = dupe


def copy(parent, collection, linked=False, replacer=None, share_materials=True):
	assert parent != collection
	dupe_lut = defaultdict(lambda: None)

	def _copy(parent, collection, linked=False):
		cc = bpy.data.collections.new(replacer(collection.name))
		copy_objects(collection, cc, linked, dupe_lut, replacer, share_materials)

		for c in collection.children:
			_copy(cc, c, linked)

		parent.children.link(cc)

	_copy(parent, collection, linked)

	# fix parenting to use a duped parent instead
	for ob, dupe in tuple(dupe_lut.items()):
		if isinstance(ob, bpy.types.Object):
			parent = dupe_lut[ob.parent]
			if parent:
				dupe.parent = parent
